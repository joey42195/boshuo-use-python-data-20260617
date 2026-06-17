
# -*- coding: utf-8 -*-

"""
2-4-3分箱
"""

import pandas as pd


# 1. 載入資料
df = pd.read_csv('E-commerce_Dirty_Dataset.csv')


# 前置安全轉型（確保數值欄位乾淨，避免 NaN 與髒字串干擾，沿用第 2 章成果）
df['age'] = pd.to_numeric(df['age'], errors='coerce')
df['income'] = pd.to_numeric(df['income'], errors='coerce')
# 順便剃除不合理的負數收入地雷（確保統計分位數正確）
df = df[df['income'] > 0]

# ---------------------------------------------------------------------
# 實戰一：pd.cut() 固定區間分箱 ➔ 應用於具備社會常識的「年齡層」
# ---------------------------------------------------------------------
print("\n實戰一 使用 pd.cut() 將連續年齡切分為『四大黃金世代』：")

# 設定自定義的年齡邊界與商業標籤
age_bins = [0, 30, 45, 60, 120]  #bins 用來設定區間邊界
# labels 用來設定對應名稱
age_labels = ['18-30 青年世代', '31-45 中堅主力', '46-60 黃金熟齡', '61+ 銀髮樂活']

df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels)

# 觀察分箱後的世代分布
age_distribution = df['age_group'].value_counts().sort_index()
print(age_distribution)



# ---------------------------------------------------------------------
# 實戰二：pd.qcut() 等頻分箱 ➔ 應用於貧富極其不均的「收入欄位」
# ---------------------------------------------------------------------
print("\n" + "-" * 80)
print("實戰二 使用 pd.qcut() 依照分位數將收入切分為『四大財富階層』：")
print("-" * 80)

# 使用 q=4（四分位數），將用戶精準切成等比例的 4 個 bin
# 我們賦予它商務標籤，分別對應 25%, 50%, 75%, 100% 的財富位置
income_labels = ['M1_資產底層', 'M2_中產階級', 'M3_富裕階層', 'M4_頂級富豪']
df['income_tier'] = pd.qcut(df['income'], q=4, labels=income_labels)

# 驗證每個 bin 裡的人數是否「完全等比例」
income_distribution = df['income_tier'].value_counts().sort_index()
print(income_distribution)

print("\n" + "-" * 80)
print("商務交叉表 看看這四大財富階層，各自貢獻了多少的消費總額 (spending)？")
print("-" * 80)
# 將連續數值 spending 轉為數值後進行分組聚合
df['spending'] = pd.to_numeric(df['spending'], errors='coerce')
revenue_contribution = df.groupby('income_tier')['spending'].sum()
print(revenue_contribution.round(2))
