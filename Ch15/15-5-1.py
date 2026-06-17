# -*- coding: utf-8 -*-

"""
15-5-1補救成本vs.利潤增量—建立財務歸因公式
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

# 1. 計算各組在 T1 觀察期的淨貢獻 (毛利 - 補償金 - 人力成本)
# 假設客服時薪人力成本為 300 元
LABOR_COST_PER_HOUR = 300

# 整理服務成本
df_service_costs = df_service.groupby('User_ID').agg({
    'Compensation_Value': 'sum',
    'Handling_Time_Hrs': 'sum'
}).reset_index()
df_service_costs['Total_Service_Cost'] = (
    df_service_costs['Compensation_Value'] + 
    (df_service_costs['Handling_Time_Hrs'] * LABOR_COST_PER_HOUR)
)

# 2. 計算 T1 毛利 (Amount - Cost)
df_post_profit = df_sales[
    df_sales['Order_Date'] >= T_EVENT
].copy()

df_post_profit['Gross_Profit'] = (
    df_post_profit['Amount'] - df_post_profit['Cost']
)

user_post_profit = df_post_profit.groupby('User_ID')[
    'Gross_Profit'
].sum().reset_index()


# 將 cohort、利潤與成本整合成完整分析框架：
df_roi = df_final_cohort[
    ['User_ID', 'Experiment_Group', 'Member_Level']
].merge(user_post_profit, on='User_ID', how='left').fillna(0)

df_roi = df_roi.merge(
    df_service_costs[
        ['User_ID', 'Total_Service_Cost']
    ],
    on='User_ID',
    how='left'
).fillna(0)

# 計算淨價值 (Net Value)
df_roi['Net_Value'] = (
    df_roi['Gross_Profit'] - df_roi['Total_Service_Cost']
)

# 計算各組平均 ROI (相對於 Failed Group 的增量)
baseline_profit = df_roi[
    df_roi['Experiment_Group'] == 'Failed Group'
]['Gross_Profit'].mean()

recovered_data = df_roi[
    df_roi['Experiment_Group'] == 'Recovered Group'
]

incremental_profit = recovered_data['Gross_Profit'].mean() - baseline_profit
avg_service_cost = recovered_data['Total_Service_Cost'].mean()

print(f"服務補救平均 ROI: {incremental_profit / avg_service_cost:.2f}")

