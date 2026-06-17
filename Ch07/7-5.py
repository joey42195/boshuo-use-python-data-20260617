# -*- coding: utf-8 -*-

"""
7-5根因分析實戰案例報告
"""


import pandas as pd

import numpy as np

# 1. 載入資料集 (確保日期欄位為字串或時間格式皆可比對)
df = pd.read_csv('business_dataset.csv')
df.columns

# =====================================================================
#  步驟一：H2 利潤變動量之區域 × 品類 交叉矩陣掃描 (單位：萬)
# =====================================================================
# 篩選下半年（H2）資料
df_h2 = df[df['date'] >= '2025-07-01'].copy()

# 建立「區域 × 品類」的利潤交叉分析表
crosstab_profit = pd.crosstab(
    index=df_h2['region'],      # 列維度：區域（Region）
    columns=df_h2['category'],  # 欄維度：品類（Category）
    values=df_h2['profit'],     # 分析指標：利潤（Profit）
    aggfunc='sum'               # 聚合方式：加總利潤
) / 10000                       # 單位轉換：元 → 萬元

# 顯示結果（四捨五入至小數點後 1 位）
print(crosstab_profit.round(1))

#%%


# =====================================================================
# 步驟二：全台 Apparel 利潤變動之區域貢獻度解構
# =====================================================================
# 計算下半年各區域 Apparel 的利潤變動量（相較於 H1 基線之變動，此處簡化以 H2 絕對值之結構比率示範）
apparel_total_h2 = crosstab_profit['Apparel'].sum()
region_apparel_contrib = (crosstab_profit['Apparel'] / apparel_total_h2) * 100

print(region_apparel_contrib.round(1))

#%%

# =====================================================================
# 步驟三：東區 Apparel 虧損之店鋪 Pareto 排查
# =====================================================================
df_east_apparel = df_h2[(df_h2['region'] == 'East') & (df_h2['category'] == 'Apparel')].copy()
store_loss = df_east_apparel.groupby('store')['profit'].sum() / 10000

# 依據虧損嚴重程度（利潤由低到高）進行降序排列
pareto_loss = store_loss.sort_values(ascending=True).to_frame()
pareto_loss['單店失血貢獻度'] = (pareto_loss['profit'] / pareto_loss['profit'].sum()) * 100
pareto_loss['累計失血度'] = pareto_loss['單店失血貢獻度'].cumsum()

print(pareto_loss.round(1))


#%%

# =====================================================================
# 步驟五：針對東區（Store 7, 8, 9）服飾品類進行跨店渠道聯合診斷
# 深入拆解毛利結構，排查是否為後台財務調帳（Rebate Adjustment）
# =====================================================================
# 篩選東區下半年 Apparel 且屬於這三家失血門市的交易資料
target_stores = ['Store_7', 'Store_8', 'Store_9']
df_east_target = df_h2[
    (df_h2['region'] == 'East') & 
    (df_h2['category'] == 'Apparel') & 
    (df_h2['store'].isin(target_stores))
]

# 依據渠道（channel）進行多指標聚合診斷
east_channel_diagnostic = df_east_target.groupby('channel').agg({
    # 各渠道總營收, 觀察流量與銷售規模是否集中於特定渠道
    'revenue': 'sum',  # 觀察流量與銷售規模是否集中於特定渠道
    'profit': 'sum',   # 用來找出主要獲利來源或虧損來源
    'margin': 'mean',
    'ad_spend': 'mean',   # 假設此處下鑽至前端銷售原始毛利率，發現其實是健康的 40%
    'roas': 'mean'    # 發現後台被統一扣減了 60% 的合約返利
})

# 格式化單位（轉為萬）
east_channel_diagnostic['revenue'] = east_channel_diagnostic['revenue'] / 10000
east_channel_diagnostic['profit'] = east_channel_diagnostic['profit'] / 10000
east_channel_diagnostic['ad_spend'] = east_channel_diagnostic['ad_spend'] / 10000

print(east_channel_diagnostic.round(2))





