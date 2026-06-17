# -*- coding: utf-8 -*-

"""
15-2-3沉默的代價—當離開沒有被說出口
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

df_sales = df_sales.sort_values(['User_ID', 'Order_Date'])


#%%

# 15-2-3 量化「沈默成本」：流失機率的熱點分析

# 找出在 Post-Event 期間完全沒下單的人 (流失客戶)
post_event_users = df_sales[df_sales['Period'] == 'Post-Event']['User_ID'].unique()
all_users = df_users['User_ID'].unique()
churned_users = set(all_users) - set(post_event_users)

# 計算各等級會員的流失率
df_users['Is_Churned'] = df_users['User_ID'].isin(churned_users)
churn_summary = df_users.groupby('Member_Level')['Is_Churned'].mean()

print("各等級會員沈默流失率：")
print(churn_summary)