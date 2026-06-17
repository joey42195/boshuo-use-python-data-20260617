# -*- coding: utf-8 -*-

"""
9-5-2利用A/B測試科學驗證漏斗優化成效
"""

import pandas as pd

# 讀取 A/B 測試實驗階段日誌
df_ab = pd.read_csv('funnel_AB.csv')

# 篩選出行動端且到達結帳頁面的使用者工作階段
df_mobile_checkout = df_ab[
    (df_ab['device'] == 'mobile') &
    (df_ab['event'] == 'begin_checkout')
]

# 初始化用於儲存統計矩陣的 Python 字典
test_data = {'Treatment': {'checkout': 0, 'purchase': 0},
             'Control': {'checkout': 0, 'purchase': 0}}


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
    
    # 將數據動態寫入字典，拒絕人工複製數字
    test_data[group]['checkout'] = total_checkout
    test_data[group]['purchase'] = total_purchase
    
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

# ==========================================
# 2. 矩陣自動對接與 Z 檢定 (統計推論階段)
# ==========================================

# 從字典中動態抽取數值，自動建立 Z 檢定所需的 NumPy 陣列
# 陣列結構嚴格對齊：[實驗組(Treatment), 對照組(Control)]
successes = np.array([
    test_data['Treatment']['purchase'],
    test_data['Control']['purchase']
])

samples = np.array([
    test_data['Treatment']['checkout'],
    test_data['Control']['checkout']
])

# 執行雙樣本比例 Z 檢定 (雙尾檢定)
z_stat, p_value = proportions_ztest(
    successes,
    samples,
    alternative='two-sided'   # 雙尾檢定（Two-Tailed Test）
)

print("=== A/B 測試雙樣本 Z 檢定自動化報告 ===")
print(f"動態成功轉化人數 矩陣 (successes) : {successes}")
print(f"動態實驗總樣本數 矩陣 (samples)   : {samples}")
print(f"Z 檢定統計量 (Z-score)             : {z_stat:.4f}")
print(f"顯著性 P 值 (P-value)                : {p_value:.10e}")