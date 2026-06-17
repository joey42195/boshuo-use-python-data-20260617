# -*- coding: utf-8 -*-

"""
15-4-1再購頻次與存活分析—預測未來的購買節奏
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 1. 載入資料
df_users = pd.read_csv('users.csv')
df_sales = pd.read_csv('sales.csv', parse_dates=['Order_Date'])
df_service = pd.read_csv('service_logs.csv', parse_dates=['Complaint_Date'])
# 上一小節的資料
df_final_cohort = pd.read_pickle("df_final_cohort.pkl")
# 2. 定義時間窗口 (以 2026-01-01 為事件基準點)
T_EVENT = pd.to_datetime('2026-01-01')
T0_START = T_EVENT - pd.Timedelta(days=90)
T1_END = T_EVENT + pd.Timedelta(days=90)


#%%

# 我們必須計算每個用戶在事件後（Post-Event）的平均購買天數差（Days Between Orders）。
# 計算事件後每筆訂單之間的間隔
# 篩選時間並排序
df_post_sales = (
    df_sales[df_sales['Order_Date'] >= T_EVENT]
    .sort_values(['User_ID', 'Order_Date'])
)

# 再計算前後購買間隔（核心邏輯）
df_post_sales['Diff'] = (
    df_post_sales.groupby('User_ID')['Order_Date']
    .diff()
    .dt.days
)

# 貼上實驗分組標籤
interval_analysis = df_post_sales.merge(
    df_final_cohort[['User_ID', 'Experiment_Group']],
    on='User_ID'
)
# 計算組別平均值
print(interval_analysis.groupby('Experiment_Group')['Diff'].mean())
