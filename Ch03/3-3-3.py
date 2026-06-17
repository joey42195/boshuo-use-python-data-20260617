# -*- coding: utf-8 -*-

"""
3-3-3分佈類—直方圖與箱型圖
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 設定繁體中文與負號支援
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# 1. 載入營運資料集
df = pd.read_csv("Store_Item_Demand.csv")
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# 數據治理：動態偵測最新營運年份，並鎖定 Store 1 進行分佈分析
latest_year = df['date'].dt.year.max()
analysis_df = df[(df['date'].dt.year == latest_year) & (df['store'] == 1)].copy()

# 設定繁體中文與負號支援
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# 統一色彩美學 (專業深藍與對比橘)
hist_color = '#34495e'
box_color = '#e67e22'


# ==========================================
# 獨立圖 (A): 直方圖 (Histogram) ➔ 觀察「數據體型」
# ==========================================
plt.figure(figsize=(8, 6.5), facecolor='white')  # 獨立建立圖 A 的畫布

# 繪製直方圖（Histogram）
# 用來觀察數據分布情形：
# 例如資料集中區域、偏態、是否存在多峰結構等
sns.histplot(    
    data=analysis_df,   # 使用的資料表(DataFrame)    
    x='sales',          # X 軸：銷售量（數值資料）    
    bins=30,            # 將數據切成 30 個區間（Bins）    
    kde=True,           # 加入 KDE 平滑曲線（觀察整體分布趨勢）    
    color=hist_color    # 設定直方圖顏色
)

plt.title(f"圖 A：直方圖 (Store 1 銷量分佈)\n核心任務：揭露數據集中在哪個區間", fontsize=12, weight='bold', color=hist_color, pad=15)
plt.xlabel("單日銷售量 (個)", fontsize=11)
plt.ylabel("出現頻次 (次數)", fontsize=11)
plt.grid(True, linestyle=':', alpha=0.4)

plt.tight_layout()

plt.show()  # 先顯示第一張圖，關閉後才會繼續跑下一張


# ==========================================
# 獨立圖 (B): 箱型圖 (Box Plot) ➔ 觀察「極端異常」
# ==========================================
plt.figure(figsize=(6, 6.5), facecolor='white')  # 獨立建立圖 B 的畫布（寬度稍微縮小，箱型圖會更美觀）

# 繪製箱型圖，拿掉 ax 參數
# 箱型圖可以快速觀察：
# 1. 中位數（Median）
# 2. 資料分散程度
# 3. 四分位距（IQR）
# 4. 是否存在離群值（Outliers）

sns.boxplot(    
    data=analysis_df,   # 使用的資料表(DataFrame)    
    y='sales',          # Y 軸：銷售量（數值資料）
    color=box_color,    # 設定箱型圖顏色    
    width=0.4,          # 設定箱體寬度    
    fliersize=5         # 設定離群值點的大小
)

plt.title(f"圖 B：箱型圖 (Store 1 銷量離散分析)\n核心任務：識別異常極端值與變異程度", fontsize=12, weight='bold', color=box_color, pad=15)
plt.ylabel("單日銷售量 (個)", fontsize=11)
plt.xlabel("Store 1", fontsize=11)
plt.grid(True, axis='y', linestyle=':', alpha=0.4)

plt.tight_layout()

plt.show()  # 顯示第二張圖