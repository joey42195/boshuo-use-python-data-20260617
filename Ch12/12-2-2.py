# -*- coding: utf-8 -*-

"""
12-2-2類別編碼—等級排序與市場語言轉譯
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. 環境設定與資料載入
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 載入資料集
df = pd.read_pickle('diamonds_12-2-1.pkl')
print(f"原始的資料筆數: {len(df)}")


#%%

# 12-2-2類別編碼：等級排序與One-Hot權衡

# 手動定義等級排序 (Label Encoding with Order)
cut_mapping = {"Fair": 1, "Good": 2, "Very Good": 3, "Premium": 4, "Ideal": 5}
df['cut'] = df['cut'].map(cut_mapping)

color_mapping = {"J": 1, "I": 2, "H": 3, "G": 4, "F": 5, "E": 6, "D": 7}
df['color'] = df['color'].map(color_mapping)

clarity_mapping = {"I1": 1, "SI2": 2, "SI1": 3, "VS2": 4, "VS1": 5, "VVS2": 6, "VVS1": 7, "IF": 8}
df['clarity'] = df['clarity'].map(clarity_mapping)

# 存成一個新的 Pickle 檔
df.to_pickle('diamonds_12-2-2.pkl')
