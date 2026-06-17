# -*- coding: utf-8 -*-

"""
8-2-3基於RFM的多維交叉排查
"""

import pandas as pd
import numpy as np

# 1. 載入資料集
df = pd.read_csv('customer_dataset.csv')
df['date'] = pd.to_datetime(df['date'])

rfm_base = pd.read_csv('rfm_base.csv')
rfm_base['date'] = pd.to_datetime(df['date'])


# 1. 將客戶層的行為標籤（customer_segment）聯結回原始交易流水帳
# 將交易明細df與RFM分群結果進行合併
df.columns
rfm_base.columns
df_txn_mixed = df.merge(
# 只取 RFM 結果中的 RFM_seg 欄位（客戶分群標籤）
    rfm_base[['customer_id', 'RFM_seg']], 
    on='customer_id',    # 以 customer_id 作為對應鍵進行資料對齊
    how='left'   # 保留所有交易資料（左表 df）
)
print(df_txn_mixed)



# 2. 【多維下鑽一】：排查各客群在各「商品品類」上的營收貢獻（轉換為萬元）
segment_product_rev = pd.pivot_table(  # 建立透視表，用於分析「客戶分群 × 商品品類」的營收結構
    df_txn_mixed,                      # 使用已合併客戶分群標籤的交易資料
    values='revenue',                 # 聚合目標：營收（revenue）
    index='RFM_seg',         # 列方向：客戶分群（VIP / 潛力 / 流失等）
    columns='product',                # 欄方向：商品品類（Electronics / Apparel 等）
    aggfunc='sum'                     # 聚合方式：計算總營收
) / 10000                             # 單位轉換：將營收由原始單位轉為「萬元」

print("=" * 60)
print("報告一：各客戶分群 x 商品品類之『營收大盤』（單位：萬元）")
print("=" * 60)
print(segment_product_rev.round(2))

# 3. 【多維下鑽二】：排查各客群在各「行銷渠道」上的平均獲利毛利率（Margin）
# 註：此處直接計算每筆交易的利潤佔營收比重
df_txn_mixed['computed_margin'] = df_txn_mixed['profit'] / df_txn_mixed['revenue']

segment_channel_margin = pd.pivot_table(  # 建立透視表，用於分析「客戶分群 × 行銷渠道」的平均毛利表現
    df_txn_mixed,                         # 使用已整合客戶分群標籤的交易資料
    values='computed_margin',            # 聚合目標：計算後的毛利率（computed_margin）
    index='RFM_seg',            # 列方向：客戶分群（VIP / 潛力 / 流失等）
    columns='channel',                   # 欄方向：行銷渠道（Direct / Email / Paid Search 等）
    aggfunc='mean'                       # 聚合方式：計算平均毛利率（反映各分群在不同渠道的獲利品質）
)


print("\n" + "=" * 60)
print("報告二：各客戶分群 x 行銷渠道之『平均毛利率』")
print("=" * 60)
print(segment_channel_margin.round(2))
print("=" * 60)



