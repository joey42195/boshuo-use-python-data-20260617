# -*- coding: utf-8 -*-

"""
6-3-2黃金交叉與趨勢轉折
"""

import pandas as pd
import matplotlib.pyplot as plt

# 1. 載入資料並聚合為「Store 1 每日總銷量」
df = pd.read_csv("Store_Item_Demand_2025.csv")
df['date'] = pd.to_datetime(df['date'])
s1_daily = df[df['store'] == 1].groupby('date')['sales'].sum().reset_index()

# 2. 核心技術：計算不同窗口的簡單移動平均 (SMA)
s1_daily['SMA_7'] = s1_daily['sales'].rolling(window=7).mean()   # 短窗口：戰術監控
s1_daily['SMA_30'] = s1_daily['sales'].rolling(window=30).mean() # 中窗口：戰略大盤

# 3. 核心技術：計算指數移動平均 (EMA) ── 越近的數據權重越高
s1_daily['EMA_7'] = (
    s1_daily['sales']
    .ewm(span=7, adjust=False)
    .mean()
)

# 4. 戰略截取：鎖定 2025 年下半年營運衝刺期（方便清晰觀測交叉與盲點）
focus_df = s1_daily[s1_daily['date'].between('2025-07-01', '2025-10-01')].copy()

# 5. 開始繪製「噪音與趨勢雷達圖」
plt.figure(figsize=(12, 7))
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# 繪製原始銷量（灰色細線，代表充斥隨機干擾的真實市場噪音）
plt.plot(focus_df['date'], focus_df['sales'], color='gray', alpha=0.3, label='原始銷量 (市場噪音)')

# 繪製移動平均線
plt.plot(focus_df['date'], focus_df['SMA_7'], color='#3498db', linewidth=2, label='7日 SMA (短窗口減震)')
plt.plot(focus_df['date'], focus_df['SMA_30'], color='#e74c3c', linewidth=2.5, label='30日 SMA (長線大盤趨勢)')
plt.plot(focus_df['date'], focus_df['EMA_7'], color='#2ecc71', linewidth=1.8, linestyle='--', label='7日 EMA (即時雷達)')

# 圖表美化與戰略定格
plt.title("Store 1 營運趨勢雷達：SMA / EMA 與雙滾動條防線", fontsize=14, weight='bold', pad=15)
plt.xlabel("營運日期", fontsize=11)
plt.ylabel("全店每日總銷量", fontsize=11)
plt.grid(True, linestyle=':', alpha=0.5)
plt.legend(loc='upper left', fontsize=10)

plt.show()

