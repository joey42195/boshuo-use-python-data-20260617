# -*- coding: utf-8 -*-

"""
6-1-2對比的五個核心維度
"""

# 3、橫向對比（Cross-sectional Comparison）—尋找內部最佳實踐

import pandas as pd

# 1. 載入時間序列資料集
df = pd.read_csv("Store_Item_Demand_2025.csv")

# 2. 鎖定 2025 年 7 月份（夏季大旺季大盤）
july_2025 = df[df['date'].between('2025-07-01', '2025-07-31')]

# 3. 計算各商店在該月份的日均總銷量
# 先將每日、各店的所有商品加總，再計算各店的月平均
daily_store_sales = (
    july_2025    #鎖定 2025 年 7 月份（夏季大旺季大盤）
    .groupby(['date', 'store'])['sales'] 
    .sum()      # 將每日、各店的所有商品加總
    .reset_index()   # 轉回 DataFrame
)


# 計算各店平均日銷量
store_rank = (
    daily_store_sales
    .groupby('store')['sales']
    .mean()
    .sort_values(ascending=False)
)

# 計算全體平均
avg_all_stores = store_rank.mean()

# 建立相對表現指數
store_performance_index = store_rank / avg_all_stores

# 5. 輸出賽馬排行榜
print("=" * 60)
print(f"2025年7月份 全國分店日均銷量排行榜 (全體平均基準: {avg_all_stores:.1f} 件)")
print("=" * 60)
for store, idx in store_performance_index.items():
    actual_sales = store_rank[store]
    print(f"店鋪代號 Store {store:02d} | 日均銷量: {actual_sales:.1f} 件 | 表現指數: {idx:.2f}")
print("=" * 60)