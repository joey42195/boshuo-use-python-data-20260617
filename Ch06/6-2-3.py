# -*- coding: utf-8 -*-

"""
6-2-3增長的陷阱—當環比與同比發生衝突
"""

import pandas as pd
import matplotlib.pyplot as plt

# 1. 載入資料
df = pd.read_csv("Store_Item_Demand_2025.csv")
df['date'] = pd.to_datetime(df['date'])

# 計算 2025 年 7 月份「所有商店 x 所有商品」組合的環比與週同比
target_date = pd.to_datetime("2025-07-11")  #  建立目標日期
yesterday_date = target_date - pd.Timedelta(days=1) # 昨日
last_week_date = target_date - pd.Timedelta(days=7) # 上週同日

# 接著，針對：商店、商品進行交叉分析
records = []
for store in df['store'].unique():
    for item in df['item'].unique():
        sub_df = df[(df['store'] == store) & (df['item'] == item)]
        
        v_today = sub_df[sub_df['date'] == target_date]['sales'].sum()
        v_yesterday = sub_df[sub_df['date'] == yesterday_date]['sales'].sum()
        v_last_week = sub_df[sub_df['date'] == last_week_date]['sales'].sum()
        
        if v_yesterday > 0 and v_last_week > 0:
            dod = (v_today / v_yesterday) - 1
            wow = (v_today / v_last_week) - 1
            records.append({
                'name': f"S{store}-I{item}", # 建立識別標籤：例如 S1-I1 代表商店1的商品1
                'DoD': dod,
                'WoW': wow,
                'sales': v_today,
                'store': store
            })

plot_df = pd.DataFrame(records)

# 2. 開始繪製高資訊密度的「四象限圖」
plt.figure(figsize=(11, 9))
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# 依據象限邏輯，動態切分顏色（讓結構一目了然）
def assign_color(row):
    if row['DoD'] >= 0 and row['WoW'] >= 0: return '#2ecc71'  # 右上：健康綠
    if row['DoD'] >= 0 and row['WoW'] < 0:  return '#f39c12'  # 右下：警告橘
    if row['DoD'] < 0  and row['WoW'] >= 0: return '#3498db'  # 左上：波動藍
    return '#e74c3c'                                         # 左下：衰退紅

plot_df['color'] = plot_df.apply(assign_color, axis=1)

# 畫出象限黃金分割線
plt.axhline(0, color='#34495e', linestyle='-', linewidth=1.5)
plt.axvline(0, color='#34495e', linestyle='-', linewidth=1.5)

# 3. 繪製散點，大小由銷量（sales）決定
plt.scatter(plot_df['DoD'], plot_df['WoW'], s=plot_df['sales']*3, 
            c=plot_df['color'], alpha=0.7, edgecolors='black', linewidths=0.8)

# 4. 核心技術：動態商業標籤演算法
for _, row in plot_df.iterrows():
    # 策略 A：如果是我們劇本的主角 S1-I1，用「黃金箭頭」進行戰略鎖定
    if row['name'] == "S1-I1":
        plt.annotate(f"★ 核心主角 {row['name']}", 
                     xy=(row['DoD'], row['WoW']), 
                     xytext=(row['DoD']+0.05, row['WoW']+0.05),
                     fontsize=11, fontweight='bold', color='black',
                     bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.8),
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.1', color='black', lw=1.5))
        continue
        
    # 策略 B：只標出核心極端值（例如雙升的前段班，或雙降的後段班），避免全圖字體塞車
    if row['DoD'] > 0.15 or row['DoD'] < -0.15 or row['WoW'] > 0.15 or row['WoW'] < -0.15:
        plt.text(row['DoD'] + 0.008, row['WoW'] + 0.008, row['name'], 
                 fontsize=9, fontweight='semibold', alpha=0.85)

# 補上商務背景文字
plt.text(0.25, 0.25, "【右上象限：雙升】\n強勁結構性成長\n➔ 應加大預算追擊", color='#1e8449', fontsize=11, ha='center', weight='bold')
plt.text(0.25, -0.25, "【右下象限：環升同降】\n促銷引起的短期假象\n➔ 檢查大盤市佔是否流失", color='#d35400', fontsize=11, ha='center', weight='bold')
plt.text(-0.25, 0.25, "【左上象限：環降同升】\n淡季常態暫時回檔\n➔ 戰略穩固無需驚慌", color='#1f618d', fontsize=11, ha='center', weight='bold')
plt.text(-0.25, -0.3, "【左下象限：雙降】\n結構性核心衰退\n➔ 立即啟動止損/斷尾", color='#922b21', fontsize=11, ha='center', weight='bold')

# 圖表美化
plt.title("2025-07-11 全國分店商品【增長四象限】戰略地圖 (已動態鎖定關鍵個體)", fontsize=14, pad=15, weight='bold')
plt.xlabel("戰術指標：日環比 (DoD)", fontsize=12, labelpad=10)
plt.ylabel("戰略指標：週同比 (WoW)", fontsize=12, labelpad=10)
plt.xlim(-0.4, 0.4)
plt.ylim(-0.4, 0.5)
plt.grid(True, linestyle=':', alpha=0.4)


print("帶有商務靈魂的標籤圖表已儲存為：advanced_growth_quadrant.png")
plt.show()