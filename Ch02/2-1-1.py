# -*- coding: utf-8 -*-
"""
2-1-1初步資料檢查
"""

import pandas as pd

# 讀入 E-commerce_Dirty_Dataset.csv
df = pd.read_csv('E-commerce_Dirty_Dataset.csv')
df.columns


print(" 檢查資料的底層骨架型態：")

# 查看前 5 筆資料
print(df.head())

# 查看資料結構資訊
print(df.info())

# 查看數值欄位統計摘要
print(df.describe())

# 檢查各欄位缺失值數量
print(df.isnull().sum())

