# -*- coding: utf-8 -*-

"""
2-4-4衍生特徵
"""

import pandas as pd
import numpy as np

# 1. 載入資料
df = pd.read_csv('E-commerce_Dirty_Dataset.csv')

# 前置安全轉型與數據排毒（沿用前幾節成果，確保運算不報錯）
df['spending'] = pd.to_numeric(df['spending'], errors='coerce')
df['visits'] = pd.to_numeric(df['visits'], errors='coerce')
df['income'] = pd.to_numeric(df['income'], errors='coerce')

# 確保分組正確、剔除負數收入與不合理值
df['user_type'] = df['user_type'].str.upper().replace({'VIP':'VIP', 'REGULAR':'Regular', 'LOW':'Low'})
df = df[(df['income'] > 0) & (df['spending'] >= 0) & (df['visits'] > 0)].copy()


# ---------------------------------------------------------------------
# 衍生特徵 1：訪問經濟效益 (Revenue per Visit)
# ---------------------------------------------------------------------
# 概念：每一次進站，該用戶平均能給平台貢獻多少真金白銀？
df['revenue_per_visit'] = df['spending'] / df['visits']
print(df[['spending', 'visits', 'revenue_per_visit']].round(2))

# ---------------------------------------------------------------------
# 衍生特徵 2：錢包份額 (Wallet Share)
# ---------------------------------------------------------------------
# 概念：該用戶在我們平台的消費，佔他總收入的百分之多少？（衡量忠誠度與開發潛力）
df['wallet_share'] = (df['spending'] / df['income']) * 100
print(df[['spending', 'income', 'wallet_share']].round(2))

# ---------------------------------------------------------------------
# 衍生特徵 3：預期補救利潤 (Expected Recovery Profit)
# ---------------------------------------------------------------------
# 核心商業邏輯：假設我們要針對 Low 用戶發放 100 元 coupon 進行挽留
# 業務現實是：挽留干預「絕不可能 100% 成功」！必須引入復甦率 (Recovery Rate)
# 我們根據行業常識，設定 VIP 的復甦率最高 (60%)，Regular 次之 (40%)，Low 最低 (15%)
# 根據商業經驗設定不同族群的預估挽回率
recovery_rate_map = {
    'VIP': 0.60,  # VIP 的復甦率最高 (60%)
    'Regular': 0.40,  # Regular 次之 (40%)
    'Low': 0.15  # Low 最低 (15%)
}

# 將商業規則映射回每位用戶
df['recovery_rate'] = (
    df['user_type']
    .map(recovery_rate_map)
)

# 設定每筆成功挽留的基礎毛利利潤為 500 元
base_profit_per_success = 500 

# 預期補救利潤 = 基礎成功利潤 * 該族群的復甦成功率
df['expected_recovery_profit'] = (
    base_profit_per_success *
    df['recovery_rate']
)


# ---------------------------------------------------------------------
# 成果展現與觀察
# ---------------------------------------------------------------------
print("\n特徵裂變成果 提取不同級別用戶的衍生特徵均值：")
print("-" * 80)

# 比較不同 user_type 的衍生特徵平均值
feature_summary = (
    df.groupby('user_type')[
        [
            'revenue_per_visit',
            'wallet_share',
            'expected_recovery_profit'
        ]
    ]
    .mean()
)
print(feature_summary.round(2))




