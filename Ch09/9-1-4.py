# -*- coding: utf-8 -*-

"""
9-1-4漏斗轉換率與流失率之雙軌計算
"""

import pandas as pd

# 載入資料
df = pd.read_csv('funnel.csv')
df.columns


#%%
# 1. 篩選出各個階段發生特定行為的獨立事件紀錄
views = df[df['event'] == 'view_item']
cart = df[df['event'] == 'add_to_cart']
checkout = df[df['event'] == 'begin_checkout']
purchase = df[df['event'] == 'purchase']

# 2. 利用 nunique() 統計各階段的不重複用戶數，建構漏斗基準表
funnel = pd.DataFrame({
    'views': [views['user_id'].nunique()],
    'cart': [cart['user_id'].nunique()],
    'checkout': [checkout['user_id'].nunique()],
    'purchase': [purchase['user_id'].nunique()]
})

# print("【漏斗各階段去重人數統計】")
# print(funnel)

#%%
"""
9-1-4漏斗轉換率計算
"""

# 計算相鄰步驟之間的轉換率
view_to_cart = funnel['cart'][0] / funnel['views'][0]
cart_to_checkout = funnel['checkout'][0] / funnel['cart'][0]
checkout_to_purchase = funnel['purchase'][0] / funnel['checkout'][0]

# 2. 計算相鄰步驟之間的流失率 (Drop-off Rate)
view_to_cart_drop = 1.0 - view_to_cart
cart_to_checkout_drop = 1.0 - cart_to_checkout
checkout_to_purchase_drop = 1.0 - checkout_to_purchase

# 3. 格式化輸出雙軌指標
print("【漏斗各階段雙軌指標檢視 (Conversion vs Drop-off)】")
print(f"商品瀏覽 ──> 加入購物車：轉換率 {view_to_cart:.2%} | 流失率 {view_to_cart_drop:.2%}")
print(f"加入購物車 ──> 開始結帳：轉換率 {cart_to_checkout:.2%} | 流失率 {cart_to_checkout_drop:.2%}")
print(f"開始結帳 ──> 完成購買：轉換率 {checkout_to_purchase:.2%} | 流失率 {checkout_to_purchase_drop:.2%}")




