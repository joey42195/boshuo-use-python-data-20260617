# -*- coding: utf-8 -*-

"""
15-4-2信任的變現能力—從客單價提升到生態系消費
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

# 1. 客單價 (AOV) 的實作
# 我們利用 Pre_Amount 與 Post_Amount 進行對比，觀察補救成功客戶是否展現出更強的消費信心。

# 1. 篩選出 Pre_Amount > 0 的既有客戶，避免除數為 0
df_active_users = df_final_cohort[df_final_cohort['Pre_Amount'] > 0].copy()

# 計算事件前後消費金額提升率
df_final_cohort['Amount_Lift'] = (
    df_final_cohort['Post_Amount']
    - df_final_cohort['Pre_Amount']
) / df_final_cohort['Pre_Amount']

# 觀察各組提升情況，
lift_summary = (
    df_final_cohort
    .groupby('Experiment_Group')['Amount_Lift']
    .describe().round(2)
)

print(lift_summary)

# 計算前後絕對金額的差額（不除以 Pre_Amount）
df_final_cohort['Amount_Delta'] = (df_final_cohort['Post_Amount'] 
                 - df_final_cohort['Pre_Amount'])

# 觀察各組淨金額變動
final_result = (df_final_cohort.groupby('Experiment_Group')['Amount_Delta']
                .describe().round(2))

print(final_result)




