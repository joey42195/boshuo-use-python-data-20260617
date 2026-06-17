
# -*- coding: utf-8 -*-

"""
3-3-1比較類—柱狀圖與折線圖
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 設定繁體中文與負號支援
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False


# 1. 載入營運資料集
df = pd.read_csv("Store_Item_Demand.csv")
# 確保日期被正確解析
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# 2. 數據清洗與聚合 (篩選 2025 年 12 月份作為分析切片)
dec_2017_df = df[(df['date'].dt.year == 2025) & (df['date'].dt.month == 12)].copy()

# [圖 A 數據]：計算 12 月份「各家分店」的總銷售量
store_sales = dec_2017_df.groupby('store')['sales'].sum().reset_index()

# [圖 B 數據]：篩選出「Store 1」在 12 月的每日銷售趨勢
store1_daily = dec_2017_df[dec_2017_df['store'] == 1].groupby('date')['sales'].sum().reset_index()


# ==========================================
# 獨立圖 (A): 柱狀圖 ➔ 回答「誰比較大」
# ==========================================
plt.figure(figsize=(8, 6))  # 獨立建立圖 A 的畫布大小

# 繪製柱狀圖（Bar Chart）
sns.barplot(
    data=store_sales,       # 使用的資料表(DataFrame)
    x='store',              # X 軸：商店名稱（類別資料）
    y='sales',              # Y 軸：銷售額（數值資料）
    color='#2c3e50',       # 設定柱狀圖顏色
    edgecolor='white'      # 設定柱子邊框顏色，提升可讀性
)

plt.title("圖 A：柱狀圖 (各店當月總銷量比較)\n核心任務：回答「誰比較大、誰賣得多」", fontsize=12, weight='bold', color='#34495e', pad=15)
plt.xlabel("分店編號 (Store ID)", fontsize=11)
plt.ylabel("當月總銷售量 (個)", fontsize=11)
plt.grid(True, axis='y', linestyle=':', alpha=0.6) # 只留水平網格

plt.tight_layout()
plt.show()  # 先顯示第一張圖，關閉後才會跑下一張


# ==========================================
# 獨立圖 (B): 折線圖 ➔ 回答「變化是什麼」
# ==========================================
plt.figure(figsize=(8, 6))  # 獨立建立圖 B 的畫布大小

# 繪製折線圖（Line Chart）
sns.lineplot(
    data=store1_daily,   # 使用的資料表(DataFrame)
    x='date',            # X 軸：日期（時間序列）
    y='sales',           # Y 軸：銷售額（數值資料）
    color='#e74c3c',    # 設定折線顏色
    linewidth=2.5,      # 設定線條粗細
    marker='o'           # 在每個資料點加上圓形標記
)

plt.title("圖 B：折線圖 (Store 1 每日銷量走勢)\n核心任務：回答「趨勢是什麼、何時上下波動」", fontsize=12, weight='bold', color='#c0392b', pad=15)
plt.xlabel("日期 (2017年12月)", fontsize=11)
plt.ylabel("單日銷售量 (個)", fontsize=11)
plt.grid(True, linestyle=':', alpha=0.6)

# 旋轉日期標籤，避免文字重疊（直接作用於當前圖表 plt）
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()  # 顯示第二張圖