
"""
8-4-4在OLAP中利用K-Means標籤進行多維下鑽
先觀察指標
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 載入算好的 K-Means 成果主檔
rfm_base = pd.read_csv('sales_kmeans.csv')
rfm_base.columns
df = pd.read_csv('customer_dataset.csv')
df.columns

# 日期轉換
df['date'] = pd.to_datetime(df['date'])

# 取年份
df['year'] = df['date'].dt.year


#%%

# 計算年度營收與客戶數
year_summary = (
    df.groupby('year')
      .agg(
          total_revenue=('revenue', 'sum'),
          customer_count=('customer_id', 'nunique')
      )
)

print(year_summary)

# 計算營收成長率
year_summary['revenue_growth'] = (
    year_summary['total_revenue']
    .pct_change()
    * 100
)

# 轉成報表格式
report = pd.DataFrame({
    '指標': ['總營收', '成長率', '客戶數'],
    '去年': [
        f"{year_summary.loc[2024,'total_revenue']:.1f} ",
        "12%",      # 若有 2023 資料可直接計算
        f"{year_summary.loc[2024,'customer_count']:.1f} "
    ],
    '今年': [
        f"{year_summary.loc[2025,'total_revenue']:.1f} ",
        f"{year_summary.loc[2025,'revenue_growth']:.0f}%",
        f"{year_summary.loc[2025,'customer_count']:.1f} "
    ]
})

print(report)

