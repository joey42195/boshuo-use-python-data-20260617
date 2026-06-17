# -*- coding: utf-8 -*-

"""
12-2-3 相關性掃描—價格驅動因子與結構辨識
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. 環境設定與資料載入
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 載入資料集
df = pd.read_pickle('diamonds_12-2-2.pkl')
print(f"原始的資料筆數: {len(df)}")

#%%


# 12-2-3 相關性掃描

plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("12-2-3 鑽石特徵相關性矩陣")
plt.show()

# 2. 移除共線性特徵 (x, y, z)
# 我們捨棄這些欄位，因為克拉已經代表了它們的綜合體積資訊
df = df.drop(['x', 'y', 'z'], axis=1)

# 3. 檢查最終特徵列表
print("目前的特徵欄位：", df.columns.tolist())
print(df.head())

#%%
# 儲存為 Pickle 檔案
df.to_pickle('diamonds_cleaned.pkl')
print("預處理完成，數據已精煉並安全封裝至 diamonds_cleaned.pkl")

