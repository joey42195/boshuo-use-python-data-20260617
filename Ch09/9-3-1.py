# -*- coding: utf-8 -*-


"""
9-3時間維度下的漏斗動態觀測
"""

import pandas as pd

# 載入包含時間戳記的資料（假設資料中有 timestamp 欄位）
df = pd.read_csv('funnel.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 1. 提取每個用戶第一次「加購」與第一次「購買」的時間
# 找出每位使用者第一次加購時間
cart_events = (
    df[df['event'] == 'add_to_cart']
    .groupby('user_id')['timestamp']
    .min()
    .reset_index()
)
# 找出每位使用者第一次購買時間
purchase_events = (
    df[df['event'] == 'purchase']
    .groupby('user_id')['timestamp']
    .min()
    .reset_index()
)

# 2. 合併資料表並計算時間差（Time Delta）
merged_time = pd.merge(
    cart_events,
    purchase_events,
    on='user_id',
    suffixes=('_cart', '_purchase')
)
# 接著計算時間差：
merged_time['days_to_purchase'] = (
    merged_time['timestamp_purchase']
    - merged_time['timestamp_cart']
).dt.total_seconds() / 86400

# 3. 區間分組統計，觀察累積轉換比例
bins = [0, 1, 3, 7, 14, 30, float('inf')]
labels = ['24小時內', '1-3天', '4-7天', '8-14天', '15-30天', '30天以上']
merged_time['conversion_window'] = pd.cut(merged_time['days_to_purchase'], bins=bins, labels=labels)


# 統計各時間窗分布，
print("【用戶從加購到購買的時間窗分佈】")
window_counts = (
    merged_time['conversion_window']
    .value_counts()
    .reindex(labels)
)
window_pct = (window_counts / len(merged_time)).map('{:.2%}'.format)   #計算占比：
distribution_df = pd.DataFrame({'用戶數': window_counts, '佔比': window_pct})
print(distribution_df)


#%%
"""
微觀時間窗分析：當行為高度集中於 24 小時內
"""

# [承接前段步驟 2] 計算出 days_to_purchase 後，將其轉換為「小時」與「分鐘」
merged_time['hours_to_purchase'] = merged_time['days_to_purchase'] * 24.0
merged_time['minutes_to_purchase'] = merged_time['days_to_purchase'] * 1440.0

# 1. 設計微觀時間區間（以小時、分鐘為切片基準）
# 分組邏輯：10分鐘內、10-30分鐘、30-60分鐘、1-3小時、3-12小時、12-24小時
bins_micro = [0, 10, 30, 60, 180, 720, 1440]
labels_micro = ['10分鐘內 (衝動型)', '10-30分鐘', '30-60分鐘', '1-3小時', '3-12小時', '12-24小時']

# 2. 進行微觀切片
merged_time['micro_window'] = pd.cut(merged_time['minutes_to_purchase'], bins=bins_micro, labels=labels_micro)

print("【用戶從加購到購買的微觀時間窗分佈】")
micro_counts = merged_time['micro_window'].value_counts().reindex(labels_micro)

# 處理可能的極端 NaN 值並補 0
micro_counts = micro_counts.fillna(0).astype(int)
micro_pct = (micro_counts / len(merged_time)).map('{:.2%}'.format)

micro_distribution_df = pd.DataFrame({'用戶數': micro_counts, '佔比': micro_pct})
print(micro_distribution_df)



