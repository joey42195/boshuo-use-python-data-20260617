# -*- coding: utf-8 -*-

"""
2-3-1離群值檢測方法
"""

import pandas as pd

# 1. 載入資料
df = pd.read_csv('E-commerce_Dirty_Dataset.csv')


# 為了確保計算精準，先將 conversion_rate 與 spending 轉為數值型態（排除 NaN 影響）
df['conversion_rate'] = pd.to_numeric(df['conversion_rate'], errors='coerce')
df['spending'] = pd.to_numeric(df['spending'], errors='coerce')

# ---------------------------------------------------------------------
# IQR 核心演算法：計算轉化率 (conversion_rate) 的邊界防線
# ---------------------------------------------------------------------
# 1. 計算第 25 百分位數 (Q1) 與 第 75 百分位數 (Q3)
Q1 = df['conversion_rate'].quantile(0.25)
Q3 = df['conversion_rate'].quantile(0.75)

# 2. 計算四分位距 (IQR = Q3 - Q1)
IQR = Q3 - Q1

# 3. 根據統計標準，建立極端值的「上下界防線」 (常數設為 1.5)
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print(f"統計防線 conversion_rate 的 IQR 圍捕戰略參數：")
print(f"   - 25% 水平線 (Q1) : {Q1 * 100:.2f}%")
print(f"   - 75% 水平線 (Q3) : {Q3 * 100:.2f}%")
print(f"   - 四分位距 (IQR)  : {IQR * 100:.2f}%")
print(f"   - 正常範圍邊界   : [{lower_bound * 100:.2f}% 至 {upper_bound * 100:.2f}%]")

# ---------------------------------------------------------------------
# 揪出資料集中突破天際的黑天鵝
# ---------------------------------------------------------------------
# 找出高於天際線（upper_bound）或低於地平線（lower_bound）的異常資料點
# 建立離群值條件
outliers_condition = (
    (df['conversion_rate'] < lower_bound) |
    (df['conversion_rate'] > upper_bound)
)

# 篩選離群資料
df_outliers = df[outliers_condition]

print(f"\n資料集中共有 {len(df_outliers)} 筆資料突破了 IQR 防線！")
print(f"   - 這些離群值的轉化率平均值高達: {df_outliers['conversion_rate'].mean() * 100:.2f}%")
print(f"   - 撈出其中前 5 筆：")
print(df_outliers[['user_id', 'user_type', 'conversion_rate']].head(5))




