# -*- coding: utf-8 -*-

"""
8-3-5客戶生命週期價值的動態估算
"""

import pandas as pd
import numpy as np

pd.set_option('display.width', None)

# 設定欄位不換行（讓所有欄位排在同一列）
pd.set_option('display.expand_frame_repr', False)

# 1. 載入資料並轉換時序格式
df_txn = pd.read_csv('customer_dataset.csv')
df_txn['date'] = pd.to_datetime(df_txn['date'])

# 2. 依據每位客戶的首購日期（資料集中的最小日期）作為基準起點
customer_first_sale = (
    df_txn
    .groupby('customer_id')['date']
    .min()
    .to_frame()
    .rename(columns={'date': 'first_buy_date'})
)

# 3. 將首購起點黏回交易流水帳中，並計算「每筆交易發生在客戶加入後的第幾天」
df_ltv = df_txn.merge(
    customer_first_sale,
    on='customer_id',
    how='left'
)


# 接著計算：得到客戶在加入後第幾天發生這筆交易。
df_ltv['days_since_signup'] = (
    df_ltv['date']
    - df_ltv['first_buy_date']
).dt.days

# 4. 定義時間窗口，觀察客戶在 30天、90天、180天 內的累計利潤貢獻 (LTV)
windows = [30, 90, 180]
ltv_results = []

# 5. 分別計算各個時間窗口內的客戶累計利潤
for days in windows:
    # 篩選在時間窗口內發生的交易
    df_window = df_ltv[df_ltv['days_since_signup'] <= days]
    
    # 計算每位客戶在此窗口內的利潤總和
    user_profit = (df_window.groupby(['customer_id','segment_true'])['profit']
                   .sum()
                   .reset_index()
                   )
    
    # 計算不同真實客群（segment_true）的「平均利潤貢獻」作為 LTV
    group_ltv = (user_profit.groupby('segment_true')['profit']
                 .mean()
                 .to_frame()
                 .rename(columns={'profit': f'LTV_{days}D'}  ) )
    ltv_results.append(group_ltv)

# 6. 合併多個窗口的 LTV 數據
final_ltv_report = pd.concat(ltv_results, axis=1)

print("=" * 60)
print("LTV 報告：不同歷史特徵客群之動態生命週期價值（單位：元）")
print("=" * 60)
print(final_ltv_report.round(1))
print("=" * 60)