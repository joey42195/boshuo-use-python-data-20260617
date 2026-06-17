# -*- coding: utf-8 -*-

"""
8-2-1 RFM的商業邏輯
"""

import pandas as pd

# 1. 載入資料集
df = pd.read_csv('customer_dataset.csv')
df.columns
df['date'] = pd.to_datetime(df['date'])

# 確保數值型欄位型態正確
df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
df['recency_days'] = pd.to_numeric(df['recency_days'], errors='coerce')


# 2. 設定觀測基準日 (Snapshot Date)
# 自動抓取資料集的最後一天，並精準加上 1 天
snapshot_date = df['date'].max() + pd.Timedelta(days=1)

# 3. 客戶行為指標時序聚合 (Standard RFM Aggregation)
# R: 動態基準日減去每位客戶最大（最新）的交易日期
# F: 累計交易次數 (txn_id 的 count)
# M: 營收總額 (revenue 的 sum)
rfm_base = df.groupby('customer_id').agg({
    'date': lambda x: (snapshot_date - x.max()).days,  # 動態計算 Recency 天數
    'txn_id': 'count',             # F：指定觀測期間內的累計購買次數
    'revenue': 'sum'               # M：指定觀測期間內的累計消費總額
}).rename(columns={
    'date': 'recency',
    'txn_id': 'frequency',
    'revenue': 'monetary'
})

# 4. 進階商務下鑽：計算客單價 (AOV) 結構
rfm_base['AOV'] = (rfm_base['monetary'] / rfm_base['frequency']).round(2)
    
print("標準 RFM 基礎行為特徵矩陣表（前 5 筆客戶）")
print("=" * 80)
print(rfm_base.head().round(2))  

    
    
    