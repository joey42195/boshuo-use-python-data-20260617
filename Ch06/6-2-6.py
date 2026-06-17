

# -*- coding: utf-8 -*-
"""
 6-2-6 滾動同比 (Rolling YoY) — 穿透隨機噪音實作
"""

import pandas as pd
import numpy as np

# 1. 載入五年期零售資料集
df = pd.read_csv("Store_Item_Demand_2021_2025.csv")
df['date'] = pd.to_datetime(df['date'])

# 2. 聚合為月度總銷量
df_monthly = df.groupby(['year', 'month'])['sales'].sum().reset_index()
# 建立月份欄位
df_monthly['月份'] = df_monthly['year'].astype(str) + '-' + df_monthly['month'].astype(str).str.zfill(2)
# 按時間排序
df_monthly = df_monthly.sort_values('月份').reset_index(drop=True)

# =====================================================================
# 核心技術：計算「傳統單月同比」vs「3個月滾動同比」
# =====================================================================

# 指標 A：標準單月同比 (YoY) -> 與 12 個月前比
# 傳統單月同比
df_monthly['單月同比(%)'] = (
    df_monthly['sales'].pct_change(12) * 100
).round(1)

# 指標 B：高階滾動同比 (3-Month Rolling YoY)
# Step 1: 計算當期「連續3個月」的累計總銷量（包含本月與前兩個月）
# 計算連續3個月的滾動累積銷量
df_monthly['3個月滾動累計銷量'] = (
    df_monthly['sales']
    .rolling(window=3)
    .sum()
)

# Step 2: 拿「3個月滾動累計銷量」去與「12個月前（去年同期）」的移動累積量算同比
# 計算3個月滾動同比
df_monthly['3個月滾動同比(%)'] = (
    df_monthly['3個月滾動累計銷量']
    .pct_change(12) * 100  #與 12 個月前的「3 個月累積窗口」相比
).round(1)

# =====================================================================
# 3. 對比：鎖定 2025 年 8 月的前後時空對照
# =====================================================================
# 過濾出 2025 年 6 月到 11 月的數據，看滾動同比的效果
report_months = ['2025-06', '2025-07', '2025-08', '2025-09', '2025-10', '2025-11']
report = df_monthly[df_monthly['月份'].isin(report_months)]

print("【全站營運診斷：單月同比 vs 3個月滾動同比】")
print(report[['月份', 'sales', '單月同比(%)', '3個月滾動累計銷量', '3個月滾動同比(%)']].to_string(index=False))