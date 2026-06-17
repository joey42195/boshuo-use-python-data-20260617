# -*- coding: utf-8 -*-

"""
3-4-4關聯類—散點圖與氣泡圖
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. 載入營運資料集
df = pd.read_csv("Store_Item_Demand.csv")
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# 數據治理：聚合資料，找出不同品項在「同一天、同一店」的銷量關聯
store1_df = df[df['store'] == 1].copy()
item1_sales = store1_df[store1_df['item'] == 1].set_index('date')['sales']
item2_sales = store1_df[store1_df['item'] == 2].set_index('date')['sales']

# 合併數據並增加一個「總銷量」維度作為氣泡大小
corr_df = pd.DataFrame({'Item_1': item1_sales, 'Item_2': item2_sales}).dropna()
corr_df['Total_Store_Sales'] = corr_df['Item_1'] + corr_df['Item_2']

# 設定繁體中文與負號支援
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False


# ==========================================
# 獨立圖 (A): 散點圖 (Scatter Plot) ➔ 尋找兩變數趨勢
# ==========================================
plt.figure(figsize=(8, 6.5), facecolor='white')  # 獨立建立圖 A 的畫布

# 散點圖（Scatter Plot）
# 用來觀察兩個變數之間是否存在趨勢或關聯性

sns.scatterplot(    
    data=corr_df,       # 使用的資料表(DataFrame)    
    x='Item_1',         # X 軸：品項 A 銷量    
    y='Item_2',         # Y 軸：品項 B 銷量
    color='#3498db',    # 點的顏色    
    alpha=0.6,          # 點的透明度（避免重疊過深）    
    edgecolor='w'       # 點的白色邊框，提升辨識度
)

plt.title("圖 A：散點圖 (品項 1 vs 品項 2)\n核心任務：回答「兩者是否有正向或負向關係」", 
          fontsize=12, weight='bold', color='#2980b9', pad=15)
plt.xlabel("品項 1 單日銷量", fontsize=11)
plt.ylabel("品項 2 單日銷量", fontsize=11)
plt.grid(True, linestyle=':', alpha=0.4)

plt.tight_layout()

plt.show()  # 先顯示第一張圖，關閉後才會跑下一張


# ==========================================
# 獨立圖 (B): 氣泡圖 (Bubble Chart) ➔ 加入第三維度
# ==========================================
# 因為右圖旁邊有圖例(Legend)，寬度微調至 9.5 讓比例更舒適
plt.figure(figsize=(9.5, 6.5), facecolor='white')  # 獨立建立圖 B 的畫布

# 氣泡圖（Bubble Chart）
# 在散點圖基礎上加入第三維度（氣泡大小）
sns.scatterplot(    
    data=corr_df,                    # 使用的資料表(DataFrame)    
    x='Item_1',                      # X 軸：品項 A 銷量    
    y='Item_2',                      # Y 軸：品項 B 銷量    
    size='Total_Store_Sales',        # 氣泡大小：總銷售量    
    sizes=(20, 300),                 # 氣泡大小範圍    
    hue='Total_Store_Sales',         # 使用顏色表示總銷售量    
    palette='viridis',               # 色彩映射方案 
    alpha=0.6,                       # 透明度    
    edgecolor='none'                 # 移除邊框避免視覺干擾
)

plt.title("圖 B：氣泡圖 (加入總銷量維度)\n核心任務：加入第三維度（氣泡大小）觀察規模效應", 
          fontsize=12, weight='bold', color='#27ae60', pad=15)
plt.xlabel("品項 1 單日銷量", fontsize=11)
plt.ylabel("品項 2 單日銷量", fontsize=11)

# 圖例優化：利用 plt.legend 控制全域圖例位置
plt.legend(title="總銷量規模", bbox_to_anchor=(1.02, 1), loc='upper left')
plt.grid(True, linestyle=':', alpha=0.4)

plt.tight_layout()

plt.show()  # 顯示第二張圖