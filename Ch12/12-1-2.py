# -*- coding: utf-8 -*-

"""
12-1-2 數據初步檢查
"""
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


# 1. 環境設定與資料載入
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False


# 1、結構與型態檢視 (Structure Check)

# 載入鑽石資料集
diamonds = sns.load_dataset('diamonds')

# 1. 檢視基本資訊
print(diamonds.info())

# 2. 類別欄位分佈檢查
print(diamonds['cut'].value_counts())
print(diamonds['color'].value_counts()) 
print(diamonds['clarity'].value_counts())


#%%

# 2、商務邏輯的一致性 (Logic Consistency)
# 鑽石是實體，物理維度不應為零。此外，我們要驗證「克拉」與「物理長寬高」是否具備邏輯一致性。

# 1. 偵測隱形鑽石（長寬高為 0）
invalid_diamonds = diamonds[(diamonds['x'] == 0) | (diamonds['y'] == 0) | (diamonds['z'] == 0)]
print(f"異常鑽石筆數：{len(invalid_diamonds)}")

# 2. 價格分佈診斷：是否有不合理的超高價或超低價
print(diamonds['price'].describe())


#%%

# 3、視覺化診斷：觀察價格與重量的關係
# 在動手建模前，先畫一張「克拉 vs 價格」的散佈圖。這張圖將成為你的「價值地圖」。

sns.scatterplot(data=diamonds.sample(2000), x='carat', y='price', alpha=0.5)
plt.title("12-1-2 價值地圖：克拉與價格的初步聯動")

plt.show()


