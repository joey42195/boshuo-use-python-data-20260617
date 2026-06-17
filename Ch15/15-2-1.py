# -*- coding: utf-8 -*-

"""
15-2-1服務補救悖論的定義—危機中的忠誠度飛躍
"""

import pandas as pd
import matplotlib.pyplot as plt

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 在進入分析前，我們先載入資料並進行基礎的處理。分析師的首要任務是建立一個「時間基準」，將數據對齊到服務事件發生的時刻。

# 14-1-1 數據對齊與「階梯式跳躍」的可視化
# 我們在理論中提到，Recovered 組會出現業績的跳躍。這在程式上需要透過「事件前後（Pre vs Post）」的對比來呈現。

# 1. 載入資料 (假設已存檔)
df_sales = pd.read_csv('sales.csv', parse_dates=['Order_Date'])
df_users = pd.read_csv('users.csv')

# 2. 標註事件前後 (基準點為 2026-01-01)
base_date = pd.to_datetime('2026-01-01')
df_sales['Period'] = df_sales['Order_Date'].apply(
    lambda x: 'Pre-Event' if x < base_date else 'Post-Event'
)

# 3. 結合用戶分組資訊 
# 我們透過 df_service_logs 的滿意度來定義 Recovered 客戶
df_analysis = pd.merge(
    df_sales,
    df_users[['User_ID', 'Member_Level']],
    on='User_ID',
    how='left'
)

# 4. 計算各組平均客單價 (AOV) 的變化
aov_change = df_analysis.groupby(['User_ID', 'Period'])['Amount'].mean().unstack()
aov_change['Change_Rate'] = (
    aov_change['Post-Event'] - aov_change['Pre-Event']
) / aov_change['Pre-Event']

print("平均客單價變動概況：")
print(aov_change['Change_Rate'].describe())

