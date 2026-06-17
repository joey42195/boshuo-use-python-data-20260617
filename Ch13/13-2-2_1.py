# -*- coding: utf-8 -*-

"""
13-2-2 觀察平穩性
1、視覺觀察
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False



# 1. 數據讀取與排序

df = pd.read_csv('ts_sales.csv', parse_dates=['date'])
df_coffee = df[df['product'] == 'coffee_machine'].copy()
df_coffee['date'] = pd.to_datetime(df_coffee['date'])
df_coffee = df_coffee.sort_values('date')

# 2. 開始繪圖
plt.figure(figsize=(14, 7))

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 支援繁體中文
plt.rcParams['axes.unicode_minus'] = False              # 正常顯示負號

# 繪製原始藍線
plt.plot(df_coffee['date'], df_coffee['units'], color='blue', marker='o', markersize=3, linestyle='-', label='咖啡機原始銷量')

# --- 加上輔助線與診斷標註 ---

# 輔助線 A：前 200 天的基準期均值 (大約在 40 左右)
baseline_mean = df_coffee['units'].iloc[:200].mean()
plt.axhline(y=baseline_mean, xmin=0, xmax=200/365, color='green', linestyle='--', linewidth=2, 
            label=f'基準期歷史均值 ({baseline_mean:.1f})')

# 輔助線 B：促銷期 40 天的突變均值 (大約在 110 左右)
promo_mean = df_coffee['units'].iloc[200:241].mean()
# 轉換對應的時間軸位置以利精準繪製橫線
promo_start_date = df_coffee['date'].iloc[200]
promo_end_date = df_coffee['date'].iloc[240]
plt.hlines(y=promo_mean, xmin=promo_start_date, xmax=promo_end_date, color='red', linestyle='--', linewidth=2, 
           label=f'促銷期突變均值 ({promo_mean:.1f})')

# 輔助線 C：整體微幅上升的趨勢（利用第一天與最後一天的 trend 機制繪製斜線）
# 用以向讀者證明除了促銷，背景還有一個緩步長高的趨勢
plt.plot([df_coffee['date'].iloc[0], df_coffee['date'].iloc[-1]], [38, 45], 
         color='orange', linestyle=':', linewidth=2, label='隱藏的長期成長趨勢 (Trend)')

# 加上促銷陰影區塊，強化視覺對比
plt.axvspan(promo_start_date, promo_end_date, color='red', alpha=0.1, label='促銷衝擊區 (均值飄移)')

# 設定圖表標題與標籤
plt.title('咖啡機銷售數據診斷：為什麼這張圖不能直接進模型？', fontsize=16, fontweight='bold')
plt.ylabel('每日銷量 (Units)', fontsize=12)
plt.xlabel('日期 (時間軸)', fontsize=12)
plt.legend(loc='upper left', fontsize=10)

plt.tight_layout()

plt.show()


