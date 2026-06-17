# -*- coding: utf-8 -*-

"""
7-1-1維度與指標
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

# groupby 本質上就是把維度當成觀察角度，對指標進行聚合。
# 觀察不同區域的營收
olap = df.groupby('region')['revenue'].sum()
print(olap)
# 觀察不同渠道利潤
olap = df.groupby('channel')['profit'].sum()
print(olap)
# 觀察不同站面的平均利潤
olap = df.groupby('store')['profit'].mean()
print(olap)
