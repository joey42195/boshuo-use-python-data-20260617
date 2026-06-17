# -*- coding: utf-8 -*-
"""
7-4-3四層下鑽法
"""

import pandas as pd
import numpy as np
# 1. 載入資料集 (確保日期欄位為字串或時間格式皆可比對)
df = pd.read_csv('business_dataset.csv')
df.columns

# 第一層：整體大盤確認（Overall Check）


# 全公司利潤總覽（可加時間切片）
overall = df.groupby('date')['profit'].sum().reset_index()

# 計算變動（例：前後期）
df['period'] = np.where(df['date'] < '2025-07-01', 'H1', 'H2')

overall_check = df.groupby('period')['profit'].sum()

print(overall_check)


# 第二層：地理區域拆解（Region Drill-down）
# 這一步通常會鎖定「問題區域」（例如 East）
region_check = df.groupby('region')['profit'].sum().sort_values()

# 看各區域變動（H1 vs H2）
region_pivot = pd.pivot_table(
    df,
    index='region',
    columns='period',
    values='profit',
    aggfunc='sum'
)

region_pivot['delta'] = region_pivot['H2'] - region_pivot['H1']
region_pivot = region_pivot.sort_values('delta')

print(region_pivot)

# 第三層：品類拆解（Category Drill-down）
# 找出問題品類，例如 East × Apparel
east_df = df[df['region'] == 'East']

category_pivot = pd.pivot_table(
    east_df,
    index='category',
    columns='period',
    values='profit',
    aggfunc='sum'
)

category_pivot['delta'] = category_pivot['H2'] - category_pivot['H1']
category_pivot = category_pivot.sort_values('delta')

print(category_pivot)

# 第四層：渠道歸因（Channel Root Cause）

east_apparel = df[
    (df['region'] == 'East') &
    (df['category'] == 'Apparel')
]

channel_pivot = pd.pivot_table(
    east_apparel,
    index='channel',
    columns='period',
    values='profit',
    aggfunc='sum'
)

channel_pivot['delta'] = channel_pivot['H2'] - channel_pivot['H1']
channel_pivot = channel_pivot.sort_values('delta')

print(channel_pivot)


# 自動抓最負貢獻Top 1
channel_root_cause = channel_pivot['delta'].idxmin()
print("可能根因渠道：", channel_root_cause)
