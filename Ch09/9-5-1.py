# -*- coding: utf-8 -*-

"""
9-5-1減少漏斗摩擦力的營運與產品藥方
"""

import pandas as pd

# 讀取 A/B 測試實驗階段日誌
df_ab = pd.read_csv('funnel_AB.csv')

# 篩選出行動端且到達結帳頁面的使用者工作階段
df_mobile_checkout = df_ab[
    (df_ab['device'] == 'mobile') &
    (df_ab['event'] == 'begin_checkout')
]

print("A/B 測試行動端觀測結果：")
for group in ['Control', 'Treatment']:
    # 獲取該組別進入結帳的獨立工作階段數量
    # 結帳人數（進入實驗池）, 這代表：已經進入結帳流程的使用者數
    group_sessions = df_mobile_checkout[df_mobile_checkout['ab_group'] == group]['session_id']
    total_checkout = len(group_sessions)
    
    # 計算該群使用者最終轉化為 purchase 的數量, 這代表：在該組中最終完成購買的 session 數
    total_purchase = df_ab[
        (df_ab['session_id'].isin(group_sessions)) &
        (df_ab['event'] == 'purchase')
    ].shape[0]
    conversion_rate = total_purchase / total_checkout  #轉換率計算
    
    print(f"  - [{group} 組] 結帳人數: {total_checkout} -> 購買人數: {total_purchase} | 轉化率: {conversion_rate:.2%}")