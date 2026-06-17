# -*- coding: utf-8 -*-

"""
6-1-2對比的五個核心維度
"""

# 4、結構對比（Structural Comparison）—拆解數據背後的組成結構


import pandas as pd

# 1. 載入時間序列資料集
df = pd.read_csv("Store_Item_Demand_2025.csv")

# 2. 計算各商品 (Item) 在全歷史中的總銷售貢獻，並由高到低排序
item_sales = (
    df.groupby('item')['sales']
    .sum()
    .sort_values(ascending=False)
)

# 計算累積貢獻比例
item_cum_sales = (
    item_sales.cumsum() / item_sales.sum()
)

# 定義 A 類明星商品
a_items = item_cum_sales[
    item_cum_sales <= 0.8
].index.tolist()


# 5. 在原始 DataFrame 中貼上結構標籤：是否為 A 類明星商品
df['is_star_item'] = df['item'].isin(a_items)

# 6. 鎖定我們在 6-1-3 定義的黃金週五（2025-07-11），拆解當天 Store 1 的銷量結構
target_date = "2025-07-11"
s1_today = df[(df['date'] == target_date) & (df['store'] == 1)]

# 7. 按結構標籤分群加總
structural_breakdown = s1_today.groupby('is_star_item')['sales'].sum()
total_sales = s1_today['sales'].sum()

print("=" * 60)
print(f"2025-07-11 Store 1 營收含金量「結構對比」報告")
print("=" * 60)
print(f"經算法判定，全站 A 類明星爆款商品為代號: {a_items}")
print("-" * 60)

for is_star, sales_volume in structural_breakdown.items():
    label = "A類高毛利明星商品" if is_star else "B/C類低毛利走量商品"
    percentage = sales_volume / total_sales
    print(f"{label} ➔ 銷量: {sales_volume:3d} 件 | 結構佔比: {percentage:.1%}")
print("=" * 60)