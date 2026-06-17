# -*- coding: utf-8 -*-

"""
9-3-2佇列分析與漏斗指標的時序漂移
"""


import pandas as pd
import matplotlib.pyplot as plt

# 1. 載入基準期歷史數據
df_base = pd.read_csv('funnel.csv')
df_base['timestamp'] = pd.to_datetime(df_base['timestamp'])

# 2. 提取行為發生的「日期」與「月份」作為時間軸
df_base['event_date'] = df_base['timestamp'].dt.date
df_base['event_month'] = df_base['timestamp'].dt.to_period('M')

# 3. 聚合每日各節點的獨立工作階段數 (Session Count)
df_daily = (
    df_base
    .groupby(['event_date', 'event'])['session_id']
    .nunique()
    .unstack(fill_value=0)
)

# 確保漏斗順序正確
funnel_order = ['view_item', 'add_to_cart', 'begin_checkout', 'purchase']
df_daily = df_daily.reindex(columns=funnel_order)

# 4. 計算關鍵核心指標：每日「結帳 -> 購買」的轉化率趨勢
df_daily['checkout_to_purchase_rate'] = df_daily['purchase'] / df_daily['begin_checkout']

print("每日結帳轉換率局部縱覽：")
print(df_daily['checkout_to_purchase_rate'].tail(5))