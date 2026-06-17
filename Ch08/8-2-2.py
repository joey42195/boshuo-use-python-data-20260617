# -*- coding: utf-8 -*-

"""
8-2-2建立客戶分群矩陣—將行為數據轉譯為營運戰略
"""

import pandas as pd
import numpy as np

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

print("步驟一：完成客戶層級 RFM 指標聚合（前 5 筆）")
print(rfm_base.head().round(1))
print("-" * 60)

#%%


# 4. 五分位數法評分 (Quantile Scoring)
# 使用 pd.qcut 將 R、F、M 分別切成 5 個等份，給予 1~5 分
# 注意：Recency 天數越小代表越活躍，因此分數應該越高（labels=[5, 4, 3, 2, 1]）
rfm_base['R_Score'] = pd.qcut(rfm_base['recency'], q=5, labels=[5, 4, 3, 2, 1]).astype(int)
# Frequency 與 Monetary 則是數值越大價值越高（labels=[1, 2, 3, 4, 5]）
# 為了避免 F 重複值過多導致 qcut 報錯，此處使用 rank(method='first') 進行平滑處理
rfm_base['F_Score'] = pd.qcut(rfm_base['frequency'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm_base['M_Score'] = pd.qcut(rfm_base['monetary'], q=5, labels=[1, 2, 3, 4, 5]).astype(int)

# 5. 定義商業策略分群函數 (Rule-based Segmentation)
def assign_segment(row):
    r, f, m = row['R_Score'], row['F_Score'], row['M_Score']

    if r >= 4 and f >= 4 and m >= 4:
        return '核心 VIP 客戶'  # 三維皆高價值
    elif r >= 4 and f <= 3 and m >= 4:
        return '重點潛力客戶'  # 高價值但尚未形成頻率
    elif r <= 2 and f >= 3 and m >= 3:
        return '流失風險客戶'  # 過去高價值但近期沉默
    elif r <= 2 and f <= 2 and m <= 2:
        return '沉睡呆滯客戶'  # 全面低活躍
    else:
        return '一般長尾客戶'  # 常態用戶

# 6. 執行分群映射
rfm_base['RFM_seg'] = rfm_base.apply(assign_segment, axis=1)

# 7. 輸出最終商業分群矩陣統計
segment_report = rfm_base.groupby('RFM_seg').agg({
    'recency': 'mean',
    'frequency': 'mean',
    'monetary': 'mean',
    'R_Score': 'count'
}).rename(columns={'R_Score': '客戶數'}).round(1)

print("步驟二：RFM 規則式商業分群矩陣報告")
print("=" * 60)
print(segment_report)
print("=" * 60)

# 存檔，供下一小節用
rfm_base.reset_index().to_csv('rfm_base.csv', index=False, encoding='utf-8-sig')
