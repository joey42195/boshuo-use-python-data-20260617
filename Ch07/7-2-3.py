# -*- coding: utf-8 -*-
"""
7-2-3 Pareto分析—找出最值得優先處理的商品.. 約在第 85 行
"""

import pandas as pd
import numpy as np

# 1. 載入資料集 (確保日期欄位為字串或時間格式皆可比對)
df = pd.read_csv('business_dataset.csv')
df.columns

# 1. 篩選 Electronics 品類資料，並建立上下半年標籤
df_elec = df[df['category'] == 'Electronics'].copy()
df_elec['period'] = np.where(
    df_elec['date'] < '2025-07-01',
    'H1_舊期',
    'H2_新期'
)

# 2. 以店鋪與期間進行利潤聚合
store_elec = df_elec.groupby(['store', 'period'])['profit'].sum().unstack()

# 3. 計算利潤變動量並進行降序排列
store_elec['利潤變動量'] = store_elec['H2_新期'] - store_elec['H1_舊期']
pareto_df = store_elec[['利潤變動量']].sort_values(by='利潤變動量', ascending=False)

# 4. 計算單店貢獻度與累計貢獻度百分比
total_elec_change = pareto_df['利潤變動量'].sum()
pareto_df['單店貢獻度'] = (pareto_df['利潤變動量'] / total_elec_change) * 100
pareto_df['累計貢獻度'] = pareto_df['單店貢獻度'].cumsum()

# 5. 格式化輸出報表（轉為萬為單位）
pareto_report = pd.DataFrame()
pareto_report['利潤增長量'] = (pareto_df['利潤變動量'] / 10000).round(1).astype(str) + '萬'
pareto_report['單店貢獻度'] = pareto_df['單店貢獻度'].round(1).astype(str) + '%'
pareto_report['累計貢獻度'] = pareto_df['累計貢獻度'].round(1).astype(str) + '%'

print("=" * 60)
print("7-2-3 實戰：Electronics 品類之店鋪利潤增長 Pareto 排查表")
print("=" * 60)
print(pareto_report)
print("=" * 60)




