# -*- coding: utf-8 -*-

"""
1-3-5資料排序
"""

import pandas as pd

# 讀取資料
df = pd.read_csv('mock_orders.csv')
df.columns

# ==========================================
# 1-3-5 資料排序 (Sorting)
# ==========================================
print("--- 資料排序 (Sorting) 示範 ---")

# 範例一：單一欄位排序（依 Sales 銷售額「由大到小」降冪排序）
# ascending=False 代表降冪（大排到小）；預設是 True 升冪（小排到大）
df_sorted_sales = df.sort_values(by="Sales", ascending=False)
print("【依銷售額由高到低排序】前 5 筆：")
print(df_sorted_sales.head())
print("-" * 30)

# 範例二：多重欄位排序
# 先依 City（城市名稱字母/筆畫）「由小到大」排序；若城市相同，再依 Profit（利潤）「由大到小」排序
df_sorted_multi = df.sort_values(
    by=["City", "Profit"], ascending=[True, False]
)
print("【先依城市升冪，再依利潤降冪排序】後 5 筆：")
print(df_sorted_multi.tail())
print("\n" + "=" * 50 + "\n")

