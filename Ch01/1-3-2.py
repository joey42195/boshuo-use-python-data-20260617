# -*- coding: utf-8 -*-

"""
1-3-2描述性統計
"""

import pandas as pd

# 讀取資料
df = pd.read_csv('mock_orders.csv')
df.columns  # 顯示所有的欄位名稱

# ==========================================
# 1-2-2 描述性統計
# ==========================================

df['Name'].count()    #1.	數量（Count）：用來計算 非空值（Non-NaN） 的筆數
df['Profit'].sum()      # 2.	總和（Sum）：用來計算數值欄位的總和
df['Age'].mean() # 3.	平均值（Mean）：代表資料的整體平均水準，可快速了解資料的一般情況。
df['Age'].median() # 4.	中位數（Median）：表示資料排序後位於中間位置的數值

#5.	標準差與變異數（Std / Var）：用來衡量資料的分散程度。若數值越大，表示資料波動越明顯。
df['Profit'].std() # 標準差 
df['Profit'].var() # 變異數

# 6.	最大值與最小值（Max / Min）：用來觀察資料的上下界。
df['Age'].max()  
df['Age'].min() 


print("--- 描述性統計摘要 (df.describe()) ---")
df.describe()  #全體數值欄的統計摘要
# 這裡可以看到 Age 的 count 數會較少，因為排除了 NaN 空值
print(df[["Age", "Sales", "Profit"]].describe())

