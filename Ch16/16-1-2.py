# -*- coding: utf-8 -*-

"""
16-1-2數據初步檢查
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 1、結構與型態檢視 (Structure Check)
# 首先確認三張表的連通性。在高單價零售中，「線索遺失」是常見的痛點（例如：線上留資但在線下被登記為新客）。

# 載入資料集
df_leads = pd.read_csv('leads.csv')
df_leads.columns
df_digital = pd.read_csv('digital_logs.csv', parse_dates=['Timestamp'])
df_offline = pd.read_csv('offline_interactions.csv', parse_dates=['Interaction_Date'])

# 檢查 Lead_ID 在各表的覆蓋率
digital_coverage = df_digital['Lead_ID'].nunique() / df_leads['Lead_ID'].nunique()
offline_coverage = df_offline['Lead_ID'].nunique() / df_leads['Lead_ID'].nunique()

# 有多少客戶，留下了線上行為紀錄？參與過線下互動？」
print(f"線上軌跡覆蓋率: {digital_coverage:.1%}") #「有多少潛在客戶，留下了線上行為紀錄？」
print(f"線下互動參與率: {offline_coverage:.1%}") #「有多少客戶參與過線下互動？」


#%%

# 2. 驗證行為與身分是否一致
# 我們必須驗證「行為」與「身分」是否匹配。例如：一個預估年收僅 100 萬的客戶，卻頻繁查看價值 2000 萬的物件，
# 這在數據上可能被視為「愛好者」而非「潛客」。


# 計算每位潛客的行為筆數
act_counts = (
    df_digital.groupby('Lead_ID')
    .size()
    .reset_index(name='act_count')
)

# 合併潛客主檔
df_merge = pd.merge(
    df_leads,
    act_counts,
    on='Lead_ID'
)

# 比較不同收入區間的行為頻率
print(
    df_merge.groupby(
        pd.qcut(df_merge['Annual_Income_Est'], 4)
    )['act_count'].mean()
)

#%%

# 3. 視覺化診斷：看見行為的「溫度」 (Visual Diagnosis)
# 我們將繪製「行為時間分佈圖」，確認數據是否具備時間序列特徵，
# 這將是 16-3 時間衰減演算法的基礎。

# 繪製數位行為在時間軸上的密集度
plt.figure(figsize=(12, 5))
sns.histplot(data=df_digital, x='Timestamp', bins=30, kde=True, color='blue')
plt.title('行為時間分佈圖(過去 30 天)')
plt.show()



