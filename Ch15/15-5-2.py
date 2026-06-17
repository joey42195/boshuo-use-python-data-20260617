# -*- coding: utf-8 -*-

"""
15-5-2補救甜蜜點探尋—速度與金額的邊際效應
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

# 15-5-2 甜蜜點探尋：邊際效應分析
# 我們需要找出 Handling_Time_Hrs（反應速度）與 Satisfaction_Score（滿意度）之間的非線性關係。

# 繪製反應速度與滿意度的關係圖
plt.figure(figsize=(10, 6))
sns.regplot(data=df_service, x='Handling_Time_Hrs', y='Satisfaction_Score', 
            lowess=True, line_kws={'color': 'red'})
plt.axvline(x=24, color='gray', linestyle='--') # 24小時黃金線
plt.title('回應速度對客戶滿意度的影響')

plt.show()


# 補償金額的邊際遞減效應
# 我們將利用 df_service_logs，觀察 Compensation_Value 如何影響 Satisfaction_Score。

"""
補償金額的邊際遞減效應
"""

# 1. 準備數據：過濾掉沒有補償的樣本（Focus on compensation impact）
df_comp_impact = df_service[df_service['Compensation_Value'] > 0].copy()

# 2. 繪製邊際效益曲線
plt.figure(figsize=(10, 6))

# 使用二階多項式擬合來呈現遞減趨勢
sns.regplot(
    data=df_comp_impact, 
    x='Compensation_Value', 
    y='Satisfaction_Score', 
    order=2,            # 二階擬合，呈現曲線
    scatter_kws={'alpha':0.3, 'color':'gray'}, 
    line_kws={'color':'#E63946', 'lw':3}
)

# 3. 標註甜蜜點 (假設數據顯示在 200 附近斜率開始變平緩)
plt.axvline(x=200, color='#1D3557', linestyle='--', label='Sweet Spot (200)')
plt.fill_between([0, 200], 1, 5, color='green', alpha=0.05, label='High ROI Zone')

# 4. 圖表優化
plt.title('邊際效用分析：補償金額與滿意度的關係', fontsize=14)
plt.xlabel('補償金額 ($)', fontsize=12)
plt.ylabel('滿意度評分 (1-5)', fontsize=12)
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)

plt.show()


