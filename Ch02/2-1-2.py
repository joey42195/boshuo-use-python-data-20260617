
# -*- coding: utf-8 -*-

"""
2-1-2資料欄位型別與結構辨識
"""


import pandas as pd


# 1. 載入數據
df = pd.read_csv('E-commerce_Dirty_Dataset.csv')

print(df.info())   # 顯示 DataFrame 的整體結構資訊
df.dtypes   # 顯示每個欄位的資料型別（dtype）

