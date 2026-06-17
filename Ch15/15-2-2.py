# -*- coding: utf-8 -*-

"""
15-2-2期待落差與情緒槓桿—心理學視角的價值轉化
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

#%%

# 15-2-2 計算「情緒槓桿」帶來的頻次增益
# 如果客戶原本 40 天買一次，補救後變成 20 天買一次，這就是情緒轉化為行為的證據。

# 計算購買間隔 (以 User_ID 分組計算日期差)
# 依照客戶排序交易時間
df_sales = df_sales.sort_values(['User_ID', 'Order_Date'])

# 計算每筆訂單與前一次購買的時間差
df_sales['Days_Since_Last_Order'] = (
    df_sales.groupby('User_ID')['Order_Date']
    .diff()
    .dt.days
)

# 對比事件後的間隔
avg_interval_post = (
    df_sales[df_sales['Period'] == 'Post-Event']
    .groupby('User_ID')['Days_Since_Last_Order']
    .mean()
)

# 繪製分佈圖 (分析師可用此圖向老闆說明：補救成功的客戶回購節奏變快了)
plt.figure(figsize=(10, 6))
sns.histplot(avg_interval_post, kde=True, color='teal')
plt.title('事件後的購買頻率分佈圖')
plt.xlabel('天數')
plt.show()

