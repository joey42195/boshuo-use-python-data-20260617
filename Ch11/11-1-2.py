# -*- coding: utf-8 -*-

"""
11-1-2數據初步檢查
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# # 這是業界常用的公開備份路徑
# url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
# df = pd.read_csv(url)

url = "Telco-Customer-Churn.csv"
df = pd.read_csv(url)


# 1、結構與型態檢視 (Structure Check)

# 初步探索
print(df.info())
print(df.head())


#%%

# 2、商務邏輯的一致性(Logic Consistency)
# 1. 檢查流失佔比
print(df['Churn'].value_counts(normalize=True))

# 2. 檢查 TotalCharges 中的空值 (隱藏在空格中)
empty_count = (df['TotalCharges'] == " ").sum()
print(f"總資費空白筆數：{empty_count}")

#%%


# 繪製合約類型與流失的關係
sns.countplot(data=df, x='Contract', hue='Churn')
plt.title('Contract Type vs. Churn')
plt.show()


