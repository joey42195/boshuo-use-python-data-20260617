# -*- coding: utf-8 -*-

"""
15-1-2數據初步檢查
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 載入數據
df_users = pd.read_csv('users.csv')
df_sales = pd.read_csv('sales.csv', parse_dates=['Order_Date'])
df_service = pd.read_csv('service_logs.csv', parse_dates=['Complaint_Date'])

# 檢查數據：有多少比例的交易用戶曾進線客服？
complaint_rate = df_service['User_ID'].nunique() / df_users['User_ID'].nunique()
print(f"客戶進線率（投訴率）：{complaint_rate:.1%}")

#%%

# 2. 商務邏輯的一致性 (Consistency Check)
# 我們必須驗證「補償」與「滿意度」的因果邏輯。例如：是否給了高額補償（Compensation_Value > 200）的客戶，滿意度得分（Satisfaction_Score）確實顯著較高？這有助於我們排除可能的系統錄入誤差。

# 1. 準備一致性檢查數據
# 可以簡單驗證
high_comp = df_service[df_service['Compensation_Value'] > 200] 
low_comp = df_service[df_service['Compensation_Value'] <= 200] 
print(high_comp['Satisfaction_Score'].mean()) 
print(low_comp['Satisfaction_Score'].mean())


#%%

# 15-1-2 程式實作：事件對齊趨勢圖
# 這段程式碼會將 df_sales 與 df_service_logs 結合，計算「距離事件天數」，並繪製出不同分組在事件前後的累計消費走勢。

# 1. 資料預處理：合併銷售與客服資料
# 我們需要知道每個 User 的 Complaint_Date 與分組標籤
df_event_base = df_service[['User_ID', 'Complaint_Date', 'Satisfaction_Score']].copy()

# 為了簡化，我們先根據滿意度定義分組標籤
df_event_base['Group'] = df_event_base['Satisfaction_Score'].apply(
    lambda x: 'Recovered Group' if x >= 4 else 'Failed Group'
)

# 2. 將銷售資料與事件基準日縫合
df_aligned = pd.merge(df_sales, df_event_base, on='User_ID', how='left')

# 3. 計算「距離事件天數」 (Time-to-Event)
# 如果是 Normal Group (沒投訴過)，我們設定一個基準點 (2026-01-01) 作為虛擬事件日
df_aligned['Complaint_Date'] = df_aligned['Complaint_Date'].fillna(pd.to_datetime('2026-01-01'))
df_aligned['Group'] = df_aligned['Group'].fillna('Normal Group')

df_aligned['Days_from_Event'] = (df_aligned['Order_Date'] - df_aligned['Complaint_Date']).dt.days

# 4. 篩選觀察窗口：事件前後 60 天
df_plot = df_aligned[(df_aligned['Days_from_Event'] >= -60) & (df_aligned['Days_from_Event'] <= 60)].copy()

# 5. 繪製視覺化診斷圖
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")
# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 使用 lineplot 繪製趨勢，ci=None 避免計算過久，也可以開啟 ci=68 (標準誤)
sns.lineplot(data=df_plot, x='Days_from_Event', y='Amount', hue='Group', 
             style='Group', markers=False, dashes=False, lw=2)

# 標註事件中心線 (T=0)
plt.axvline(x=0, color='red', linestyle='--', alpha=0.7)
plt.text(0.5, plt.ylim()[1]*0.9, 'Service Failure Event', color='red', fontweight='bold')

# 優化圖表標籤
plt.title('視覺化論斷：客訴事件後的處理概況', fontsize=15)
plt.xlabel('客訴事件前後 60 天的平均消費額 (T=0)', fontsize=12)
plt.ylabel('平均消費額 ($)', fontsize=12)
plt.legend(title='客戶分類')

plt.show()