# -*- coding: utf-8 -*-

"""
10-1-2數據初步檢查
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 載入資料
df = pd.read_csv('cookie_cats.csv')

# 查看資料前 5 筆
print(df.head())

#%%

# 1、結構與型態檢視 (Structure Check)

# ID 唯一性
# 檢視資料型態與重複值
print(df.info())
print(f"重複的用戶數：{df['userid'].duplicated().sum()}")


# 指標型態(Boolean to Int)
df['retention_1'] = df['retention_1'].astype(np.int8)
df['retention_7'] = df['retention_7'].astype(np.int8)


#%%

# 2、樣本均衡性與隨機化檢驗 (Randomization Check)


# 1. 檢查各組樣本數
version_counts = df.groupby('version').size()
print(f"各組紀錄筆數：\n{version_counts}")

# 2. 樣本比例檢查
ratio = version_counts['gate_30'] / version_counts['gate_40']
print(f"樣本比例 (gate_30 / gate_40): {ratio:.4f}")

#%%

# 3、異常值偵測：找出「怪獸玩家」(Outlier Diagnosis)

# 檢查遊戲局數分佈 (是否有極端值)
print(df['sum_gamerounds'].describe())

# 視覺化偵測

sns.boxplot(x='version', y='sum_gamerounds', data=df)
plt.title("各組遊戲局數分佈（含離群值）")
plt.show()



#%%
# 存成一個新的 Pickle 檔，完整保留資料型別

# --- 2. 資料型態校準 (Data Typing) ---
# 將 True/False 轉為 0/1 (int8 節省空間且利於運算)

# 將版本轉為類別型態 (Categorical)
df['version'] = df['version'].astype('category')

df.to_pickle('cookie_cats_clean.pkl')






