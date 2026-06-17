# -*- coding: utf-8 -*-

"""
6-4-1指數化—看見真正的成長軌跡
"""

import pandas as pd
import matplotlib.pyplot as plt

# 1. 載入資料並確保日期格式
df = pd.read_csv("Store_Item_Demand_2025.csv")
df['date'] = pd.to_datetime(df['date'])

# 2. 篩選 Store 1，並將數據按「月份」聚合，計算各商品每月的總銷量
s1_df = df[df['store'] == 1]

# Growth Index Analysis（成長指數分析）


monthly_sales = s1_df.groupby([df['date'].dt.to_period('M'), 'item'])['sales'].sum().unstack()

# 3. 戰略截取：鎖定 2025 年下半年 (7月至12月)，觀察新一波策略的擴張速度
focus_months = monthly_sales.loc['2025-07':'2025-12']

# 4. 核心技術：指數化 (Indexing) ➔ 將 2025-07 設定為基期 100
# 利用 iloc[0] 取得第一個月的數值，透過 Pandas 的廣播機制讓整欄自動除以基期並乘以 100
base_period_value = focus_months.iloc[0]

indexed_sales = (focus_months / base_period_value) * 100

print("========== 成長指數分析結果（以 2025-07 = 100）==========")
print(" base_period_value（基期 2025-07 各商品銷量）")
print(base_period_value)

print("\n indexed_sales（各月份相對基期的成長指數）")
print(indexed_sales.round(1))
print("=======================================================")






