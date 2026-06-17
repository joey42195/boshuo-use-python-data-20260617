# -*- coding: utf-8 -*-

"""
9-2-3視覺化多維漏斗—群組對比圖實作
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 設定繁體中文自行與負號正常顯示
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 載入資料
df = pd.read_csv('funnel.csv')
df.columns


def generate_dimensional_funnel(df, dimension):
    """
    動態根據傳入的維度（Dimension），計算各子群體的步驟轉換率與去重人數
    """
    # 1. 依據維度與事件進行分組統計去重人數
    grouped = df.groupby([dimension, 'event'])['user_id'].nunique().unstack()
    
    # 2. 確保標準電商漏斗的順序
    stages = ['view_item', 'add_to_cart', 'begin_checkout', 'purchase']
    # 預防資料中漏掉特定事件，僅選取存在的欄位
    available_stages = [s for s in stages if s in grouped.columns]
    grouped = grouped[available_stages]
    
    # 3. 計算步驟轉換率 (Step Conversion Rate)
    funnel_matrix = pd.DataFrame(index=grouped.index)
    
    # 基礎用戶數
    funnel_matrix['基礎流量(View)'] = grouped['view_item']
    
    # 計算各階段步驟轉換率
    if 'add_to_cart' in grouped.columns:
        funnel_matrix['瀏覽 ──> 加購 (CR)'] = (grouped['add_to_cart'] / grouped['view_item']).map('{:.2%}'.format)
    if 'begin_checkout' in grouped.columns:
        funnel_matrix['加購 ──> 結帳 (CR)'] = (grouped['begin_checkout'] / grouped['add_to_cart']).map('{:.2%}'.format)
    if 'purchase' in grouped.columns:
        funnel_matrix['結帳 ──> 購買 (CR)'] = (grouped['purchase'] / grouped['begin_checkout']).map('{:.2%}'.format)
        
    return funnel_matrix

# ---- 實戰應用：對「裝置(device)」維度進行下鑽分析 ----
print("【維度下鑽：裝置維度 (Device) 漏斗矩陣】")
device_funnel = generate_dimensional_funnel(df, 'device')
print(device_funnel.to_string())

#%%

# ==========================================
# 建立 9-2-3 自動化多維漏斗群組對比圖
# ==========================================

# 1. 動態解析與資料清洗：將帶有 '%' 的字串轉換回 0~1 的小數浮點數
df_clean = device_funnel.copy()

# 定義要轉換的欄位對應
cr_columns = {
    '瀏覽 ──> 加購': '瀏覽 ──> 加購 (CR)',
    '加購 ──> 結帳': '加購 ──> 結帳 (CR)',
    '結帳 ──> 購買': '結帳 ──> 購買 (CR)'
}

# 再取得所有轉換階段及裝置類型的名稱
stages = list(cr_columns.keys())   # 取得所有轉換階段
all_devices = df_clean.index.tolist() # 動態取得 ['desktop', 'mobile', 'tablet']

# 用來存放重構資料的陣列
records = []

for device in all_devices:
    for stage, col_name in cr_columns.items():
        # 自動清理百分比符號並轉回小數
        val_str = df_clean.loc[device, col_name]
        conversion_rate = float(val_str.rstrip('%')) / 100.0
        drop_off_rate = 1.0 - conversion_rate
        
        # 為了美化圖表標籤，將裝置名稱轉為首字大寫顯示（如 desktop -> Desktop）
        device_label = device.capitalize()
        
        records.append({
            '階段轉換': stage,
            '裝置類型': device_label,
            '轉換率': conversion_rate,
            '流失率': drop_off_rate
        })

# 2. 自動重構為適合繪圖的 Long-format DataFrame
plot_data = pd.DataFrame(records)

y_pos = np.arange(len(stages))
# 因為裝置從 2 個變成 3 個，我們稍微調窄橫條寬度避免重疊
bar_width = 0.25  

# 3. 建立 1x2 子圖畫布（左右並排）
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# 設定三個裝置的對應顏色（深藍、清新綠、百搭灰）
colors = {'Desktop': '#2b5c8f', 'Mobile': '#48C9B0', 'Tablet': '#95A5A6'}

# --- 左圖：各裝置步驟轉換率對比 ---
for i, device in enumerate(plot_data['裝置類型'].unique()):
    device_df = plot_data[plot_data['裝置類型'] == device]
    # 計算每個裝置橫條的 Y 軸偏移量，讓三個橫條完美並列
    offset = (i - 1) * bar_width 
    
    rects = ax1.barh(y_pos + offset, device_df['轉換率'], bar_width, 
                     label=f'{device}', color=colors[device])
    
    # 為左圖加上數值標籤
    for rect in rects:
        width = rect.get_width()
        ax1.text(width + 0.01, rect.get_y() + rect.get_height()/2, f'{width*100:.1f}%',
                 ha='left', va='center', fontsize=9, fontweight='bold', color='#2C3E50')

ax1.set_yticks(y_pos)
ax1.set_yticklabels(stages, fontsize=11, fontweight='bold')
ax1.invert_yaxis()  
ax1.set_xlim(0, 1.25)
ax1.set_xlabel('步驟轉換率 (比例)', fontsize=12)
ax1.set_title('多維對比：各裝置步驟轉換率 (Conversion Rate)', fontsize=13, pad=15, fontweight='bold')
ax1.legend(loc='lower right', fontsize=11)


# --- 右圖：各裝置步驟流失率對比 ---
# 為了凸顯 Mobile 的危險流失，我們幫右圖的 Mobile 換上醒目的橘紅色
colors_drop = {'Desktop': '#b0c4de', 'Mobile': '#EC7063', 'Tablet': '#BDC3C7'}

for i, device in enumerate(plot_data['裝置類型'].unique()):
    device_df = plot_data[plot_data['裝置類型'] == device]
    offset = (i - 1) * bar_width
    
    rects = ax2.barh(y_pos + offset, device_df['流失率'], bar_width, 
                     label=f'{device}', color=colors_drop[device])
    
    # 為右圖加上數值標籤（流失率 > 50% 紅字加粗）
    for rect in rects:
        width = rect.get_width()
        text_color = '#D9383A' if (width > 0.5 and device == 'Mobile') else '#2C3E50'
        text_weight = 'bold' if (width > 0.5 and device == 'Mobile') else 'normal'
        ax2.text(width + 0.01, rect.get_y() + rect.get_height()/2, f'{width*100:.1f}%',
                 ha='left', va='center', fontsize=9, weight=text_weight, color=text_color)

ax2.set_yticks(y_pos)
ax2.set_yticklabels([])  
ax2.invert_yaxis()
ax2.set_xlim(0, 1.25)
ax2.set_xlabel('步驟流失率 (比例)', fontsize=12)
ax2.set_title('多維對比：各裝置步驟流失率 (Drop-off Rate)', fontsize=13, pad=15, fontweight='bold')
ax2.legend(loc='lower right', fontsize=11)

# 4. 調整總排版並儲存
plt.suptitle("裝置維度多維漏斗群組對比圖 (動態三維相容版)", fontsize=16, fontweight='bold', y=1.05)
plt.tight_layout()
plt.show()