# -*- coding: utf-8 -*-
"""
11-2-1數值型特徵的陷阱
"""


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

url = "Telco-Customer-Churn.csv"
df = pd.read_csv(url)


# 1、結構與型態檢視 (Structure Check)

# 初步探索
print(df.info())
print(df.head())

#%%


# 11-2-1 數值型特徵的陷阱：處理資費的偏態與缺失值
# 在這一節，我們解決 TotalCharges 的型別危機，並透過數學轉換讓特徵更穩定。

# 1. 處理 TotalCharges 的字串空格地雷
# 歸因：tenure=0 的新用戶尚未產生費用，填補為 0
df['TotalCharges'] = df['TotalCharges'].replace(" ", "0").astype(float)

# 2. 觀察偏態（Skewness）
df[['tenure','MonthlyCharges','TotalCharges']].describe()
print(f"TotalCharges 原始偏度: {df['TotalCharges'].skew():.2f}")


# 存成一個新的 Pickle 檔，完整保留資料型別與分級標籤
df.to_pickle('Telco-Customer-Churn_11-2-1.pkl')





