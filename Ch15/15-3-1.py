# -*- coding: utf-8 -*-

"""
15-3-1回顧性隊列的建構—從歷史資料中重建實驗
"""

import pandas as pd
import numpy as np

# 1. 載入資料
df_users = pd.read_csv('users.csv')
df_sales = pd.read_csv('sales.csv', parse_dates=['Order_Date'])
df_service = pd.read_csv('service_logs.csv', parse_dates=['Complaint_Date'])

# 2. 定義時間窗口 (以 2026-01-01 為事件基準點)
T_EVENT = pd.to_datetime('2026-01-01')
T0_START = T_EVENT - pd.Timedelta(days=90)
T1_END = T_EVENT + pd.Timedelta(days=90)

# 3. 計算每個用戶在 T0 與 T1 的總消費 (歸納行為特徵)
# 計算每個用戶在 T0 與 T1 的總消費
sales_t0 = df_sales[
    (df_sales['Order_Date'] >= T0_START) & 
    (df_sales['Order_Date'] < T_EVENT)
].groupby('User_ID')['Amount'].sum().rename('Pre_Amount')

sales_t1 = df_sales[
    (df_sales['Order_Date'] >= T_EVENT) & 
    (df_sales['Order_Date'] <= T1_END)
].groupby('User_ID')['Amount'].sum().rename('Post_Amount')

# 合併回用戶主檔
# 先將Cohort資料融合，也就是把使用者基本資料（df_users）、
# T0消費（Pre_Amount）、T1消費（Post_Amount）
# 整合成一張「可分析的cohort表」以建立實驗母體。
df_cohort = df_users.merge(sales_t0, on='User_ID', how='left') \
                    .merge(sales_t1, on='User_ID', how='left') \
                    .fillna(0)

# 4. 根據客服紀錄進行分組標籤
# 取得有投訴的用戶及其滿意度
service_status = df_service.groupby('User_ID')['Satisfaction_Score'].max()

# 最後，依據服務結果進行分組，使整個資料結構具備實驗語義。
def label_groups(row):
    uid = row['User_ID']
    if uid not in service_status:
        return 'Smooth Group'
    elif service_status[uid] >= 4:
        return 'Recovered Group'
    else:
        return 'Failed Group'

df_cohort['Experiment_Group'] = df_cohort.apply(label_groups, axis=1)

print(df_cohort['Experiment_Group'].value_counts())


