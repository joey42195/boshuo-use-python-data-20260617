# -*- coding: utf-8 -*-

"""
1-3-4條件式資料過濾
"""

import pandas as pd

# 讀取資料
df = pd.read_csv('mock_orders.csv')
df.columns

# ==========================================
# 1-3-4 條件過濾
# ==========================================

# 條件過濾指的是：利用布林條件（True / False）篩選資料列，例如：
# 寫法一：先建立布林條件，再套用篩選
condition = df['Age'] > 30   # 年齡大於 30
df_filtered = df[condition]  # 套用條件
print(df_filtered)

# 寫法二：直接在括號中套用條件
high_year = df[df['Year'] > 2025]  # 直接套用條件
print(high_year.head())   # 顯示前 5 筆資料

print("--- 3. 條件過濾 (年齡大於 30 且 銷售額高於 5000) ---")
# 多重條件過濾：& (且), | (或)，條件必須加括號
condition = (df["Age"] > 30) & (df["Sales"] > 5000)
filtered_df = df[condition]
print(f"符合條件的資料共有 {len(filtered_df)} 筆。使用 iloc 取出前 3 筆：")
print(filtered_df.iloc[0:3])  # iloc 含頭不含尾，序號0、1、2的資料

# Age 大於 30 或者是 Sales > 5000
filtered_df = df[(df["Age"] > 30) | (df["Sales"] > 5000)]
print(f"符合條件的資料共有 {len(filtered_df)} 筆")
print(filtered_df.sample(5))  # sample 隨機取出5筆

