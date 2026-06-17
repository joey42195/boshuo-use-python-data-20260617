# -*- coding: utf-8 -*-

"""
9-1-3從事件流建立漏斗
"""

import pandas as pd

# 載入資料
df = pd.read_csv('funnel.csv')
df.columns

"""
一、 確立漏斗的核心事件
"""
# 查看事件類型
# 檢查資料集中的事件類型與基礎計數
print("【事件類型分布檢視】")
print(df['event'].value_counts())

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

print("【漏斗各階段去重人數統計】")
print(funnel)



