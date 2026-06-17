# -*- coding: utf-8 -*-

"""
15-3-2排除異常值與偏誤
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
df_cohort = df_users.merge(sales_t0, on='User_ID', how='left') \
                    .merge(sales_t1, on='User_ID', how='left') \
                    .fillna(0)

# 4. 根據客服紀錄進行分組標籤
# 取得有投訴的用戶及其滿意度
service_status = df_service.groupby('User_ID')['Satisfaction_Score'].max()

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



#%%
"""
# 15-3-2 排除異常值與偏誤
"""

# 14-2-3 提到的「惡意客訴者」，在數據上有一條非常清晰的「貢獻度邊界線」。

# 2. 排除異常值的 Python 實作
# 這段程式碼演示了如何精確剔除那些「高貢獻但負利潤」的偽忠誠客戶。

# 彙整每個用戶的總補償與總利潤
user_comp = df_service.groupby('User_ID')['Compensation_Value'].sum()
# 接著計算客戶實際創造的總利潤：
user_profit = (
    df_sales.assign(
        Profit=df_sales['Amount'] - df_sales['Cost']
    )
    .groupby('User_ID')['Profit']
    .sum()
)

# 將兩者整合後形成利潤檢查表：
df_margin_check = pd.DataFrame({
    'Total_Comp': user_comp,
    'Total_Profit': user_profit
}).fillna(0)

# 找出「薅羊毛」嫌疑人：補償金佔利潤比超過 50% 者
suspected_hunters = df_margin_check[
    df_margin_check['Total_Comp']
    > df_margin_check['Total_Profit'] * 0.5
].index

# 從 Cohort 中移除污染樣本
df_final_cohort = df_cohort[
    ~df_cohort['User_ID'].isin(suspected_hunters)
].copy()

print(
    f"剔除惡意客訴者後剩餘樣本數: "
    f"{len(df_final_cohort)}"
)


#%%
# 保留 pandas 資料型態，先儲存，下一小節用
df_final_cohort.to_pickle("df_final_cohort.pkl")


