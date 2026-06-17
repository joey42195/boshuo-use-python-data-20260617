# -*- coding: utf-8 -*-

"""
1-3-7 Pandas樞紐分析表
"""

import pandas as pd


# 讀取資料
df = pd.read_csv('mock_orders.csv')
df.columns


# ==========================================
# 1-2-7 Pandas 樞紐分析表 (pivot_table)
# ==========================================
print("--- 5. 樞紐分析表 (列：年度, 欄：商品類別, 值：銷售總和) ---")
count_table = pd.pivot_table(
    df,             # 原始資料（DataFrame）
    index="Year",   # 列索引：依「年度」分組，形成列
    columns="Category", # 欄索引：依「類別」分類
    values="Sales",  # 用來「統計」的欄位
    aggfunc="sum"  # 聚合函數：計算每個 年度×類別的總和
)

print(count_table)



# 統計各年度、各類別的訂單數量
pivot_count = pd.pivot_table(
    df,
    index="Year",           # 列索引：年度
    columns="Category",     # 欄索引：商品類別
    values="Sales",       # 統計Sales
    aggfunc="count"         # 計算數量
)

# 顯示結果
print(pivot_count)


