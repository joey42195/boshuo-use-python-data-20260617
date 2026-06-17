# -*- coding: utf-8 -*-

"""
5-2-1常見抽樣方法
"""

import pandas as pd
import numpy as np

# 固定隨機種子確保可重現性
np.random.seed(42)

# 1. 載入全功能統計資料集
df = pd.read_csv("comprehensive_market_stats.csv")


# =====================================================================
# 技術一：隨機抽樣 (Simple Random Sampling) ── 機率均等
# =====================================================================
# 商業場景：從全站 12,730 筆訂單中，無差別隨機抽取 100 筆做快速品質稽核
random_sample = df.sample(n=100, random_state=42)

print("【1. 隨機抽樣結果】")
print(f"成功抽取樣本數: {len(random_sample)} 筆")
print(f"樣本平均消費金額: {random_sample['最終消費金額(元)'].mean():.1f} 元 (全站母體平均: {df['最終消費金額(元)'].mean():.1f} 元)")
print("-" * 70 + "\n")


# =====================================================================
# 技術二：分層抽樣 (Stratified Sampling) ── 捍衛少數關鍵族群的代表性
# =====================================================================
# 商業場景：依「會員年資」將顧客分層為 新進/中堅/元老VIP，確保高價值 VIP 不被隨機雜訊淹沒
# 先在記憶體中建立分層標籤 (不破壞原始 CSV)
def assign_tier(years):
    if years <= 2: return '新進會員(0-2年)'
    elif years <= 5: return '中堅會員(3-5年)'
    else: return '元老級VIP(6-9年)'

df['_會員分層'] = df['會員年資(年)'].apply(assign_tier)

# 觀察母體原本的結構比例
print("【2. 分層抽樣 ── 母體結構觀察】")
print(df['_會員分層'].value_counts(normalize=True).round(3) * 100)

# 各層嚴格依比例 (frac=0.01，即各抽 1%) 進行抽樣
stratified_sample = df.groupby('_會員分層', group_keys=False).sample(frac=0.01, random_state=42)

print("\n【分層抽樣後的樣本結構比例】")
print(stratified_sample['_會員分層'].value_counts(normalize=True).round(3) * 100)
print(f"成功分層抽取總樣本數: {len(stratified_sample)} 筆")
print("-" * 70 + "\n")


# =====================================================================
# 技術三：群集抽樣 (Cluster Sampling) ── 降低跨渠道/區域的調查成本
# =====================================================================
# 商業場景：廣告渠道（紅/藍/綠版位）分散。我們隨機抽中「一個渠道」，對該渠道做 100% 全量大體檢
all_clusters = df['廣告版位設計'].unique()

# 隨機抽取 1 個廣告版位作為目標群集
# 隨機從所有廣告版位（群集）中抽取 1 個版位
selected_cluster = np.random.choice(
    all_clusters,   # 所有可被抽樣的群集（廣告版位清單）
    size=1,         # 抽取 1 個群集
    replace=False   # 不可重複抽樣（避免同一群集被重複選中）
)

# 保留這個被抽中渠道內的所有消費者資料
cluster_sample = df[df['廣告版位設計'].isin(selected_cluster)]

print("【3. 群集抽樣結果】")
print(f"隨機抽中的幸運市場群集 (Cluster): {selected_cluster}")
print(f"該群集內涵蓋的總訂單量 (全量調查): {len(cluster_sample)} 筆")
print(f"該群集的平均消費金額: {cluster_sample['最終消費金額(元)'].mean():.1f} 元")
print("=" * 70)