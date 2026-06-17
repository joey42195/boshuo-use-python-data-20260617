# -*- coding: utf-8 -*-

"""
1-3-6分組與聚合(Groupby)
"""

import pandas as pd

# 讀取資料
df = pd.read_csv('mock_orders.csv')
df.columns


# ==========================================
# 1-2-6 分組與聚合 (groupby + agg)
# ==========================================
print("--- 4. 分組與聚合 (依城市分組，計算銷售總和與平均利潤) ---")

# 範例一：依 City 欄位分組，並對Sales'欄位進行加總
result = df.groupby(['City'])['Sales'].sum()   
print(result)
print("\n" + "=" * 50 + "\n")

# 範例二：按 City 和 Year 分組，並對Sales欄位進行加總
result = df.groupby(['City','Year'])['Sales'].sum()
print(result)
print("\n" + "=" * 50 + "\n")

# 分組後的結果有時會形成階層索引（MultiIndex），
# 若希望轉回一般DataFrame格式，可使用 reset_index()。
result = df.groupby(['City','Year'])['Sales'].sum().reset_index()
print(result)
print("\n" + "=" * 50 + "\n")

#%%

# 進階聚合工具：agg()

group_result = (
    df.groupby("City")
    .agg({"Sales": "sum", "Profit": "mean"})
    .reset_index()  # 將階層索引轉回一般 DataFrame
)
print(group_result)
print("\n" + "=" * 50 + "\n")

