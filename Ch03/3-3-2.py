# -*- coding: utf-8 -*-

"""
3-3-2組成類—堆疊圖、圓餅圖與環形圖
"""

import matplotlib.pyplot as plt
import pandas as pd

# 設定繁體中文與負號支援
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# 1. 載入營運資料集
df = pd.read_csv("Store_Item_Demand.csv")
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# 篩選 2025 年下半年 (7月~12月) 作為分析區間
df_2017_h2 = df[(df['date'].dt.year == 2025) & (df['date'].dt.month >= 7)].copy()
df_2017_h2['month'] = df_2017_h2['date'].dt.month

# 聚合計算：看 Item 1, 2, 3 這三個核心品項在各月份的總銷量
pivot_df = df_2017_h2[df_2017_h2['item'].isin([1, 2, 3])].groupby(['month', 'item'])['sales'].sum().unstack().fillna(0)

# [圖 A 數據]：時間序列堆疊（各月份 7~12）
months = pivot_df.index
item1_sales = pivot_df[1].values
item2_sales = pivot_df[2].values
item3_sales = pivot_df[3].values

# [圖 B 數據]：鎖定 12 月份的單點組成比例
dec_sales = pivot_df.loc[12].values
labels_b = ['品項 1', '品項 2', '品項 3']

# 統一商務美學色彩 (莫蘭迪高雅色系)
composition_colors = ['#2c3e50', '#3498db', '#bdc3c7']


# ==========================================
# 獨立圖 (A): 堆疊面積圖 ➔ 觀察「隨時間的組成變化」
# ==========================================
plt.figure(figsize=(8, 6.5), facecolor='white')  # 獨立建立圖 A 的畫布

# 使用 plt.stackplot 繪製堆疊面積
plt.stackplot(months, item1_sales, item2_sales, item3_sales, 
              labels=['品項 1', '品項 2', '品項 3'], 
              colors=composition_colors, alpha=0.85)

plt.title("圖 A：堆疊面積圖 (2025 下半年銷量趨勢)\n核心任務：觀察各組成部分隨「時間」的消長變化", fontsize=12, weight='bold', color='#34495e', pad=15)
plt.xlabel("月份 (2025年)", fontsize=11)
plt.ylabel("總銷售量 (個)", fontsize=11)
plt.xlim(7, 12)
plt.xticks(range(7, 13), [f"{x}月" for x in range(7, 13)])
plt.grid(True, linestyle=':', alpha=0.4)
plt.legend(loc='upper right', fontsize=10)

plt.tight_layout()

plt.show()  # 先顯示第一張圖，關閉後才會繼續跑下一張


# ==========================================
# 獨立圖 (B): 圓餅圖 ➔ 觀察「單一時間點的比例結構」
# ==========================================
plt.figure(figsize=(8, 6.5), facecolor='white')  # 獨立建立圖 B 的畫布

# 使用 pie() 繪製圓餅圖，並透過 width 參數改成環形圖（Donut Chart）
# 繪製圓餅圖（Pie Chart）
plt.pie(    
    dec_sales,                     # 各分類數值（決定扇形大小）    
    labels=labels_b,             # 各分類名稱    
    autopct='%1.1f%%',         # 顯示百分比（保留 1 位小數）    
    startangle=90,             # 從正上方開始繪製    
    colors=composition_colors,         # 設定扇形顏色    
    wedgeprops={
        'edgecolor': 'white',  # 扇形之間加入白色邊框
        'linewidth': 2         # 邊框粗細
    },    
    textprops={
        'fontsize': 11,        # 文字大小
        'fontweight': 'bold'   # 粗體字
    }
)

# 設定標題
plt.title(
    '不同會員等級占比',
    fontsize=16,
    fontweight='bold'
)

# 讓圓餅圖保持正圓形
plt.axis('equal')

# 顯示圖表
plt.show()



# ==========================================
# 獨立圖 (C): 環形圖 ➔ 觀察「單一時間點的比例結構」
# ==========================================
plt.figure(figsize=(8, 6.5), facecolor='white')  # 獨立建立圖 B 的畫布

# 使用 pie() 繪製圓餅圖，並透過 width 參數改成環形圖（Donut Chart）
wedges, texts, autotexts = plt.pie(    
    dec_sales,                 # 各分類數值（決定扇形大小）    
    labels=labels_b,           # 每個分類名稱（顯示在圖外）    
    autopct='%1.1f%%',         # 顯示百分比格式（保留 1 位小數）    
    startangle=90,             # 從 90 度開始旋轉（讓圖表從正上方開始）    
    colors=composition_colors, # 設定各區塊顏色    
    # 設定文字樣式
    textprops={
        'fontsize': 11,        # 字體大小
        'fontweight': 'bold',  # 粗體
        'color': '#2c3e50'     # 字體顏色
    },    
    pctdistance=0.8,           # 百分比文字距離中心的位置    
    labeldistance=1.15,        # 標籤距離圓心的位置（避免擠在一起）    
    # wedgeprops：設定扇形樣式
    wedgeprops=dict(
        width=0.4,             # 關鍵：挖空中心，形成環形圖
        edgecolor='white',     # 扇形之間加入白色邊框
        linewidth=2            # 邊框粗細
    )
)

# 微調環形內的百分比字體顏色為白色
plt.setp(autotexts, size=10, weight="bold", color="white")

plt.title("圖 B：環形圖 (2025/12 單月銷量構成)\n核心任務：剖析「特定時間點」的份額與比例結構", fontsize=12, weight='bold', color='#2c3e50', pad=15)

plt.tight_layout()

plt.show()  # 顯示第二張圖