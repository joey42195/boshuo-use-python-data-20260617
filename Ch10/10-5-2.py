# -*- coding: utf-8 -*-
"""
10-5-2依玩家涉入程度分群分析
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False


# 載入原始資料
df = pd.read_pickle('cookie_cats_clean.pkl')
df.columns


# 1. 將遊玩局數細分為：新手(0-30), 中階(30-100), 高階(100+)
bins = [0, 30, 100, float('inf')]
labels = ['新手 (0-30)', '中階 (30-100)', '高階 (100+)']
df['player_segment'] = pd.cut(df['sum_gamerounds'], bins=bins, labels=labels)

# 2. 計算每個分群在不同版本的留存率
pivot_table = df.pivot_table(index='player_segment', 
                             columns='version', 
                             values='retention_7', 
                             aggfunc='mean')

# 3. 計算 Gate 40 相對於 Gate 30 的提升率 (Uplift)
pivot_table['uplift'] = (pivot_table['gate_40'] - pivot_table['gate_30']) / pivot_table['gate_30']

print("各分群留存率與提升率矩陣：")

print(pivot_table)

# 4. 視覺化：受傷最重的區間一目了然
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
sns.heatmap(pivot_table[['uplift']], annot=True, fmt=".2%", cmap='RdYlGn', center=0)
plt.title("Gate 40 對不同玩家分群的衝擊 (Uplift %)")

plt.show()