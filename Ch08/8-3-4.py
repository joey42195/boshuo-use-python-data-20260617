# -*- coding: utf-8 -*-

"""
8-3-4世代分析與時序矩陣
"""

import pandas as pd
import numpy as np

# 1. 載入資料集並確保日期格式正確
df_txn = pd.read_csv('customer_dataset.csv')
df_txn['date'] = pd.to_datetime(df_txn['date'])

# 2. 由於原始流水帳需要與客戶的「註冊時間」對齊，我們提取客群層級的 signup_date
# 實務上我們會直接從客戶主檔獲取，此處我們利用 groupby 模擬動態獲取首購/註冊月
# 為了對齊讀者產生的資料，我們將交易日期與註冊日期都縮減到「年-月」維度
df_txn['txn_month'] = df_txn['date'].dt.to_period('M')

# 假設從客戶主檔讀取 customer_df（此處直接從 txn 的真實標記或 signup 計算模擬）
# 為了完美還原，我們依據 customer_id 找出該客戶在資料集中的「最早交易月份」作為首購世代
customer_cohort = (
    df_txn                                    # 交易明細資料表
    .groupby('customer_id')['date']           # 依 customer_id 分組，取出 date 欄位
    .min()                                    # 找出每位客戶的第一筆交易日期
    .dt.to_period('M')                        # 將日期轉換為年月格式（例如 2025-03）
    .to_frame()                               # Series 轉換成 DataFrame
    .rename(columns={'date': 'cohort_month'}) # 將欄位名稱改為 cohort_month（客戶所屬 Cohort）
)
print(customer_cohort)

# 3. 將世代月份 (cohort_month) 黏回原始交易流水帳
df_cohort = df_txn.merge(customer_cohort, on='customer_id', how='left')

# 4. 計算時間跨度差 (Cohort Index)
# 計算該筆交易距離其首購世代過去了幾個月 (0 代表當月回購, 1 代表第一個月留存...)
df_cohort['cohort_index'] = (
    (df_cohort['txn_month'].dt.year -
     df_cohort['cohort_month'].dt.year) * 12 +
    (df_cohort['txn_month'].dt.month -
     df_cohort['cohort_month'].dt.month)
)

# 5. 依據 世代月份 與 跨度月 進行客戶數不重複計數 (pd.Series.nunique)
cohort_counts = (
    df_cohort.groupby(
        ['cohort_month', 'cohort_index']
    )['customer_id']
    .nunique().reset_index()
)

# 6. 利用 pivot_table 將資料展開為標準的世代矩陣 (Cohort Matrix)
cohort_matrix = cohort_counts.pivot(
    index='cohort_month',
    columns='cohort_index',
    values='customer_id'
)

# 7. 將絕對人數轉換為「留存率百分比」（以 Month 0 的總人數為分母基底）
cohort_size = cohort_matrix.iloc[:, 0] # 取得第 0 個月的初始總人數
retention_matrix = cohort_matrix.divide(cohort_size, axis=0)

print("=" * 70)
print("世代分析：電商月度客戶留存率矩陣 (Cohort Matrix) - 部分展示")
print("=" * 70)
# 展示前 6 個首購世代在後續半年的留存率表現
print(retention_matrix.iloc[:6, :7].round(3) * 100)
print("=" * 70)