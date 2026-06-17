# -*- coding: utf-8 -*-

"""
9-1-5視覺化漏斗與雙軌指標診斷
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 設定繁體中文自行
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 載入資料（保留你原本的前置處理邏輯）
df = pd.read_csv('funnel.csv')

views = df[df['event'] == 'view_item']
cart = df[df['event'] == 'add_to_cart']
checkout = df[df['event'] == 'begin_checkout']
purchase = df[df['event'] == 'purchase']

funnel = pd.DataFrame({
    'views': [views['user_id'].nunique()],
    'cart': [cart['user_id'].nunique()],
    'checkout': [checkout['user_id'].nunique()],
    'purchase': [purchase['user_id'].nunique()]
})

# 計算相鄰步驟之間的轉換率與流失率（皆為 0~1 的小數）
view_to_cart = funnel['cart'][0] / funnel['views'][0]
cart_to_checkout = funnel['checkout'][0] / funnel['cart'][0]
checkout_to_purchase = funnel['purchase'][0] / funnel['checkout'][0]

view_to_cart_drop = 1.0 - view_to_cart
cart_to_checkout_drop = 1.0 - cart_to_checkout
checkout_to_purchase_drop = 1.0 - checkout_to_purchase

# ==========================================
# 繪圖區塊
# ==========================================

stages_transform = [
    '商品瀏覽 ──> 加入購物車',
    '加入購物車 ──> 開始結帳',
    '開始結帳 ──> 完成購買'
]

# 取出先前的指標
conversion_rates = [view_to_cart, cart_to_checkout, checkout_to_purchase]  
drop_off_rates = [view_to_cart_drop, cart_to_checkout_drop, checkout_to_purchase_drop]    

y_pos = np.arange(len(stages_transform))

# 建立 1x2 子圖畫布
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

# --- 左圖：步驟轉換率（推進效率） ---
bars_conv = ax1.barh(y_pos, conversion_rates, color=['#5DADE2', '#48C9B0', '#56B4E9'], height=0.5)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(stages_transform, fontsize=11, fontweight='bold')
ax1.invert_yaxis()  
ax1.set_xlim(0, 1.2)  # 【修正】設定範圍為 0 ~ 1.2，留出 0.2 的空間放標籤文字
ax1.set_xlabel('轉換率 (比例)', fontsize=12) # 【修正】修正標籤文字為比例
ax1.set_title('各階段：步驟轉換率（Conversion Rate）\n數值越高代表推進效率越好', fontsize=13, pad=15, fontweight='bold')

# 在長條右側標註轉換率數值
for bar in bars_conv:
    width = bar.get_width()
    # 【修正】微調文字平移至 width + 0.02 處，並將數值 * 100 轉回百分比顯示
    ax1.text(width + 0.02, bar.get_y() + bar.get_height()/2, f'{width*100:.2f}%', 
             ha='left', va='center', fontsize=11, fontweight='bold', color='#2C3E50')


# --- 右圖：步驟流失率（阻力痛點） ---
bars_drop = ax2.barh(y_pos, drop_off_rates, color=['#F4D03F', '#EB984E', '#EC7063'], height=0.5)
ax2.set_yticks(y_pos)
ax2.set_yticklabels([])  
ax2.invert_yaxis()
ax2.set_xlim(0, 1.2)  # 【修正】設定範圍為 0 ~ 1.2
ax2.set_xlabel('流失率 (比例)', fontsize=12) # 【修正】修正標籤文字為比例
ax2.set_title('各階段：步驟流失率（Drop-off Rate）\n數值越高代表該步驟阻力越大', fontsize=13, pad=15, fontweight='bold')

# 在長條右側標註流失率數值
for i, bar in enumerate(bars_drop):
    width = bar.get_width()
    text_color = '#D9383A' if width > 0.5 else '#2C3E50'
    text_weight = 'bold' if width > 0.5 else 'normal'
    
    # 【修正】微調文字平移至 width + 0.02 處，並將數值 * 100 轉回百分比顯示
    ax2.text(width + 0.02, bar.get_y() + bar.get_height()/2, f'{width*100:.2f}%', 
             ha='left', va='center', fontsize=11, weight=text_weight, color=text_color)

# 3. 設定全圖總標題與版面調整
plt.suptitle("電商漏斗雙軌指標診斷圖 (Funnel Dual-Metric Analysis)", fontsize=16, fontweight='bold', y=1.05)
plt.tight_layout()

# 4. 顯示

plt.show()