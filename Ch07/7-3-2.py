"""
7-3-2實戰演練—門市營收異常診斷
"""

import pandas as pd
import numpy as np

# 1. 載入資料集 (確保日期欄位為字串或時間格式皆可比對)
df = pd.read_csv('business_dataset.csv')
df.columns


# =====================================================================
# 7-3-3 門市異常診斷實作：全通路 Z-Score 掃描與極端值定位
# =====================================================================

# 依門市聚合年度總營收
store_summary = (
    df.groupby('store')['revenue']
      .sum()
      .reset_index()
)

# 轉換為萬元單位
store_summary['revenue_wan'] = (
    store_summary['revenue'] / 10000
)

# 2. 計算全體門市營收的算術平均值與母體標準差
mean_revenue = store_summary['revenue_wan'].mean()
std_revenue = store_summary['revenue_wan'].std()

# 3. 計算各門市的 Z-Score 標準分數
store_summary['z_score'] = (store_summary['revenue_wan'] - mean_revenue) / std_revenue

# 4. 依據 Z-Score 由高到低進行降序排列
store_report = (
    store_summary
    .sort_values(by='z_score', ascending=False)
    .reset_index(drop=True)
)

# 5. 格式化輸出報表
store_report['年度總營收'] = store_report['revenue_wan'].round(1).astype(str) + '萬'
store_report['Z-Score'] = store_report['z_score'].round(2)

print("=" * 60)
print("7-3-2 全台門市年度總營收 Z-Score 異常偵測表")
print("=" * 60)
print(store_report[['store', '年度總營收', 'Z-Score']])
print("=" * 60)

#  後台排查：檢查全台店鋪與區域（Region）的隸屬關係
print(df[['region', 'store']].drop_duplicates().sort_values(by='region').reset_index(drop=True))


# 下鑽診斷：檢查營收前三名門市的月度營收波動，確認是否存在短週期異常
top_stores_monthly = df[df['store'].isin(['Store_12', 'Store_11', 'Store_10'])].groupby(['store', 'month'])['revenue'].sum().unstack()
print(top_stores_monthly)

