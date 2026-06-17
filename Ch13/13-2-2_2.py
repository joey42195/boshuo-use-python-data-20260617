# -*- coding: utf-8 -*-

"""
13-2-2 觀察平穩性
2、觀察自相關圖(ACF/PACF)
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

#%%

# 原始數據的acf，跟pacf

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# 1. 讀取數據並篩選咖啡機原始銷量
df_sales = pd.read_csv("ts_sales.csv")
df_coffee = df_sales[df_sales['product'] == 'coffee_machine'].copy()
df_coffee['date'] = pd.to_datetime(df_coffee['date'])
df_coffee = df_coffee.sort_values('date')

# 2. 開始繪製雙聯圖 (1排2列)
fig, axes = plt.subplots(1, 2, figsize=(15, 5))
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 支援繁體中文
plt.rcParams['axes.unicode_minus'] = False              # 正常顯示負號
# 設定最大延遲階數 (Lag) 為 20 天，方便肉眼觀察
max_lags = 20

# --- 左圖：原始數據 ACF ---
plot_acf(df_coffee['units'], ax=axes[0], lags=max_lags, title="原始數據 ACF (自相關函數) - 觀察緩慢衰減")
axes[0].set_ylim(-1.05, 1.05)
axes[0].set_xlabel('延遲階數 (Lags / 天)', fontsize=11)
axes[0].set_ylabel('相關係數', fontsize=11)

# --- 右圖：原始數據 PACF ---
plot_pacf(df_coffee['units'], ax=axes[1], lags=max_lags, title="原始數據 PACF (偏自相關函數)")
axes[1].set_ylim(-1.05, 1.05)
axes[1].set_xlabel('延遲階數 (Lags / 天)', fontsize=11)

# 3. 優化排版並顯示
plt.tight_layout()

plt.show()

