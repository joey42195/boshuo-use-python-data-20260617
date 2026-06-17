
# -*- coding: utf-8 -*-
"""
3-3-5時間序列類—趨勢圖與移動平均
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 設定繁體中文與負號支援
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False


# 1. 載入營運資料集
df = pd.read_csv("Store_Item_Demand.csv")
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# 數據治理：鎖定 Store 1 且 Item 1 的數據，並篩選出 2025 年整年的資料
# （對齊圖片中 X 軸 2025-01 至 2026-01 的時間範圍）
store1_item1 = df[(df['store'] == 1) & (df['item'] == 1)].copy()
store1_item1 = store1_item1[(store1_item1['date'].dt.year == 2025)].sort_values('date')

# 關鍵計算：使用 rolling 計算 7 日移動平均線
store1_item1['MA7'] = store1_item1['sales'].rolling(window=7).mean()


# ==========================================
# 獨立圖 (A): 原始趨勢圖 ➔ 觀察「看現象」
# ==========================================
plt.figure(figsize=(9, 5.5), facecolor='white')  # 建立圖 A 的畫布

# 繪製每日銷量折線圖
plt.plot(
    store1_item1['date'],      # X 軸：日期（時間序列）
    store1_item1['sales'],     # Y 軸：每日銷量數據    
    color='#34495e',           # 線條顏色（深灰藍色）
    alpha=0.5,                 # 透明度（0~1），降低透明度可弱化雜訊感    
    label='每日銷量'            # 圖例名稱（legend 顯示文字）
)

# 圖表美化與排版
plt.title("圖 A：原始趨勢圖 (Daily Sales)\n核心任務：記錄當下現象與短期波動", 
          fontsize=12, weight='bold', color='#1a252f', pad=15)
plt.ylabel("銷量 (個)", fontsize=11)
plt.grid(True, linestyle=':', alpha=0.3)
plt.legend(loc='upper right')

# 限制 X 軸範圍，讓時間對齊
plt.xlim(pd.Timestamp('2025-01-01'), pd.Timestamp('2026-01-01'))

plt.tight_layout()

plt.show()


# ==========================================
# 獨立圖 (B): 移動平均圖 ➔ 觀察「看方向」
# ==========================================
plt.figure(figsize=(9, 5.5), facecolor='white')  # 建立圖 B 的畫布

# 同時畫出淡淡的原始點與深色的平滑線，對比感極強
plt.plot(store1_item1['date'], store1_item1['sales'], 
         color='#cdd6e2', alpha=0.4, label='原始數據')

# 繪製 7 日移動平均線（Moving Average）
plt.plot(
    store1_item1['date'],      # X 軸：日期（時間序列）
    store1_item1['MA7'],       # Y 軸：7 日移動平均後的銷量
    
    color='#005088',           # 線條顏色（深藍色，用來強調主要趨勢）
    linewidth=2.5,             # 線條粗細（比原始資料更粗，凸顯趨勢線）
    
    label='7日移動平均'         # 圖例名稱（legend 顯示文字）
)

# 圖表美化與排版
plt.title("圖 B：移動平均圖 (7-Day Moving Average)\n核心任務：過濾隨機資訊，鎖定增長方向", 
          fontsize=12, weight='bold', color='#005088', pad=15)
plt.ylabel("平滑銷量 (個)", fontsize=11)
plt.grid(True, linestyle=':', alpha=0.3)
plt.legend(loc='upper right')

# 限制 X 軸範圍，讓時間對齊
plt.xlim(pd.Timestamp('2025-01-01'), pd.Timestamp('2026-01-01'))

plt.tight_layout()

plt.show()