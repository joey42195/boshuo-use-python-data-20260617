# -*- coding: utf-8 -*-

"""
7-1-2分層分析的重要性
"""

import pandas as pd
import numpy as np

# 1. 載入資料集
df = pd.read_csv('business_dataset.csv')
df.columns

# 維度
dimensions = [
    'region',
    'store',
    'category',
    'channel',
    'customer_type'
]

# 指標
metrics = [
    'revenue',
    'profit',
    'quantity'
]


#%%

# 7-1-2 分層分析的重要性

# 單一維度觀察：一定是先看總體
olap = df.groupby('channel')['revenue'].mean()
print(olap)

# 再加入分層，例如： Region：
result = pd.pivot_table(
    df,                 # 資料來源
    index='region',     # 將 region 作為列維度
    columns='channel',  # 將 channel 作為欄維度
    values='revenue',   # 統計 revenue 欄位
    aggfunc='mean'      # 對每個交叉組合計算平均營收
).round(2)

print(result)
