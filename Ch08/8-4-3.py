# -*- coding: utf-8 -*-

"""
8-4-3機器學習分群實作
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 1. 載入資料集
df = pd.read_csv('customer_dataset.csv')
df.columns
df['date'] = pd.to_datetime(df['date'])


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

    
#%%    
    
    
# 1. 延續 8-2-2 節算好的 rfm_base 基礎指標 (包含 recency, frequency, monetary)
# 為確保程式碼獨立運行，此處確保數據已準備就緒
features = ['recency', 'frequency', 'monetary']
X = rfm_base[features]

# 2. 【關鍵步驟】特徵標準化 (Scaling)
scaler = StandardScaler()  # 建立標準化器
X_scaled = scaler.fit_transform(X)  # 對特徵進行標準化


# 3. 初始化 K-Means 模型（設定群數 K=5，固定隨機種子以利復現）
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
rfm_base['Cluster'] = kmeans.fit_predict(X_scaled)

# 4. 統計各個 Cluster 的行為特徵均值與人數
cluster_summary = rfm_base.groupby('Cluster').agg({
    'recency': 'mean',
    'frequency': 'mean',
    'monetary': 'mean',
    'Cluster': 'count' # 計算人數
}).rename(columns={'customer_segment': 'Customer_Count'}).round(1)


# 定義 K-Means Cluster 與商業標籤的映射字典（依 R, F, M 特徵精準定義）
cluster_mapping = {
    0: '一般活躍客',
    1: '高活躍成長客',
    2: '流失客',
    3: '沉睡客',
    4: 'VIP'
}

# 將機器學習的冰冷代號 (0, 1, 2, 3, 4) 轉換為具有決策溫度的商業特徵標籤
cluster_summary['客群特徵解讀'] = cluster_summary.index.map(cluster_mapping)
rfm_base['Kmeans_seg'] = rfm_base.Cluster.map(cluster_mapping)

print("=" * 70)
# 5. 計算各群的營收貢獻佔比（Revenue Share）

# 全部客戶的總營收（用來當作分母）
total_revenue = rfm_base['monetary'].sum()

# 計算每個 Cluster 的營收佔比（%）
# 作法：
# 1. 先依 Cluster 加總 monetary（各群總營收）
# 2. 再除以整體總營收 total_revenue
# 3. 轉成百分比
# 4. 四捨五入到小數點後 1 位
cluster_summary['Revenue_Share(%)'] = round(
    (rfm_base.groupby('Cluster')['monetary'].sum() / total_revenue) * 100,
    1
)
print("機器學習運算產出：5 大行為 Cluster 統計特徵表")
print("=" * 70)
print(cluster_summary)
print("=" * 70)


rfm_base.reset_index().to_csv('sales_kmeans.csv', index=False, encoding='utf-8-sig')


