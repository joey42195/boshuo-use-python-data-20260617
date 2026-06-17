# -*- coding: utf-8 -*-

"""
12-2-1 數據清洗—排除異常與不合理紀錄
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. 環境設定與資料載入
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 載入資料集
df = sns.load_dataset('diamonds')
print(f"原始的資料筆數: {len(df)}")

#%%
# 1、物理維度校正：剔除「隱形鑽石」


# 1. 剔除物理長度為 0 的異常值
df = df[(df[['x', 'y', 'z']] != 0).all(axis=1)]

# 2. 處理價格為 0 或邏輯不合的數據 (diamonds 資料集通常價格正常，但實務中需檢查)
df = df[df['price'] > 0]

print(f"清洗後的資料筆數: {len(df)}")


# 2、離群值處理：修正不合理的比例結構
# 1. 定義離群值清洗函數 (基於 1.5 * IQR 準則)
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # 僅保留在合理區間內的資料
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# 2. 針對深度比 (depth) 與 檯面比 (table) 執行清洗
print(f"清洗前資料筆數: {len(df)}")

df = remove_outliers(df, 'depth')
df = remove_outliers(df, 'table')

print(f"清洗後資料筆數: {len(df)} (已排除比例異常之瑕疵鑽石)")

# 3. 視覺化驗證：觀察清洗後的數據分佈
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
sns.boxplot(x=df['depth'])
plt.title("Depth % (After Cleaning)")

plt.subplot(1, 2, 2)
sns.boxplot(x=df['table'])
plt.title("Table % (After Cleaning)")

plt.show()


# 存成一個新的 Pickle 檔
df.to_pickle('diamonds_12-2-1.pkl')

