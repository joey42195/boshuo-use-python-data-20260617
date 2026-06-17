# -*- coding: utf-8 -*-

"""
4-4-3長尾與極端群體
"""

import pandas as pd

df = pd.read_csv('eCommerceUser.csv')


# ---------------------------------------------------------------------
# 【4-4-3 長尾與極端群體】利用 Z-score 找出長尾
# ---------------------------------------------------------------------

# 手動計算 spending 的 Z-score 條件過濾
spending_mean = df['spending'].mean()
spending_std = df['spending'].std()
df_long_tail = df[(
    (df['spending'] - spending_mean) 
    / spending_std) > 3]

print(f"突破整體 3 個標準差 (Z > 3) 的極端高價值用戶：")
print(f"全站 5,128 筆中，共精準篩選出：{len(df_long_tail)} 筆黃金長尾用戶。")
print(df_long_tail[['user_type', 'income', 'visits', 'spending']].head(5)) # 先看前5筆

