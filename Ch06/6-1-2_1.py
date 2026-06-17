# -*- coding: utf-8 -*-

"""
6-1-2對比的五個核心維度
"""

# 1、時間對比（Temporal Comparison）—理解趨勢的時間座標

import pandas as pd

# 1. 載入時間序列資料集
df = pd.read_csv("Store_Item_Demand_2025.csv")

# 2. 篩選出 Store 1 的數據，並確保日期欄位為時間格式
s1_df = df[df['store'] == 1].copy()
s1_df['date'] = pd.to_datetime(s1_df['date'])

# 3. 將多個商品的銷量加總，聚合為「Store 1 全店每日總銷量」
s1_daily = s1_df.groupby('date')['sales'].sum().reset_index()

# 4. 關鍵技術：利用 shift() 進行時間平移，取得對比基準
# shift(1) 代表將數據下移 1 天，即取得「昨日銷量」
s1_daily['sales_yesterday'] = s1_daily['sales'].shift(1)
# shift(7) 代表將數據下移 7 天，即取得「上週同日銷量」
s1_daily['sales_last_week'] = s1_daily['sales'].shift(7)

# 5. 我們再加入星期欄位
s1_daily['weekday'] = s1_daily['date'].dt.day_name()

# 7. 窺探 2025 年 7 月上旬的數據導航結果
preview_cols = ['date', 'weekday', 'sales', 'sales_yesterday', 'sales_last_week']
print(s1_daily[preview_cols].iloc[185:192].to_string(index=False))