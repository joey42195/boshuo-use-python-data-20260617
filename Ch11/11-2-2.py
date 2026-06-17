# -*- coding: utf-8 -*-
"""
11-2-2類別變數的商務轉譯
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_pickle('Telco-Customer-Churn_11-2-1.pkl')


#%%

# 11-2-2 類別變數的商務轉譯：標籤編碼 vs. 獨熱編碼
# 選擇邏輯：無序的用 One-Hot，有序的用 Label Encoding。

# 直接轉換成0與1。
binary_cols = [
    'Partner',
    'Dependents',
    'PhoneService',
    'PaperlessBilling',
    'Churn'
]

for col in binary_cols:
    df[col] = df[col].map({'Yes': 1, 'No': 0})

# 具有商務順序的欄位
contract_map = {
    'Month-to-month': 0,    # 0 = 月繳
    'One year': 1,          # 1 = 一年約
    'Two year': 2           # 2 = 兩年約
}
df['Contract_encoded'] = df['Contract'].map(contract_map)


# 不具順序意義的類別欄位
df = pd.get_dummies(
    df,
    columns=['PaymentMethod',
             'InternetService'],
    dtype=int
)

# 存成一個新的 Pickle 檔，完整保留資料型別與分級標籤
df.to_pickle('Telco-Customer-Churn_11-2-2.pkl')




