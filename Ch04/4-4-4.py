# -*- coding: utf-8 -*-

"""
4-4-4群體與行為差異
"""

import numpy as np
import pandas as pd

df = pd.read_csv('eCommerceUser.csv')

# ---------------------------------------------------------------------
# 【4-4-4 群體與行為差異】結構解釋：哪一群人貢獻了什麼營運結果？
# ---------------------------------------------------------------------


# 透過 groupby 進行總體營收貢獻 (sum) 與核心效率 (mean) 的綜合提煉
df_444 = df.groupby('user_type').agg(
    total_revenue=('spending', 'sum'),        # 該群體貢獻的總營收
    avg_spending=('spending', 'mean'),        # 該群體平均客單價
    avg_conversion=('conversion_rate', 'mean') # 該群體平均轉換率
)

# 計算該群體營收佔全站總營收的百分比
total_site_revenue = df['spending'].sum()
df_444['revenue_contribution_pct'] = (df_444['total_revenue'] / total_site_revenue * 100).round(2)
df_444['total_revenue'] = df_444['total_revenue'].round(0)
df_444['avg_spending'] = df_444['avg_spending'].round(2)
df_444['avg_conversion'] = (df_444['avg_conversion'] * 100).round(2) # 轉為百分比顯示

print(df_444[['revenue_contribution_pct', 'avg_spending', 'avg_conversion']])
