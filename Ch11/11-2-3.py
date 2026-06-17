# -*- coding: utf-8 -*-
"""
11-2-3衍生特徵—從原始欄位到商業訊號的重建
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_pickle('Telco-Customer-Churn_11-2-2.pkl')

#%%

# 10-2-3 衍生特徵：創造「平均客單價」與「服務多樣性」
# 這一步是將「維度」升級為「洞察」。

# 1. 歷史忠誠度指標：每個月平均貢獻多少錢？
# (tenure + 1) 同樣是為了避免除以 0
df['Avg_Monthly_Benefit'] = df['TotalCharges'] / (df['tenure'] + 1)

# 2. 服務多樣性指標 (Bundling Count)
# 用戶在生態系中的「服務滲透程度」
service_cols = [
    'OnlineSecurity',
    'OnlineBackup',
    'DeviceProtection',
    'TechSupport',
    'StreamingTV',
    'StreamingMovies'
]

# 需查原始資料，有的欄位不只是Yes/No
# 保險做法：統一轉成 0/1
df[service_cols] = df[service_cols].replace({
    'Yes': 1,
    'No': 0,
    'No internet service': 0
})

df['Service_Count'] = df[service_cols].sum(axis=1).astype(int)

# 存成一個新的 Pickle 檔，完整保留資料型別與分級標籤
df.to_pickle('Telco-Customer-Churn_11-2-3.pkl')

