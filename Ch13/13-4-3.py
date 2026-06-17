# -*- coding: utf-8 -*-
"""
13-4-3 Auto-ARIMA實戰—季節性的影響
"""

import pandas as pd
import numpy as np
import pmdarima as pm

# =====================================================================
# 1. 載入原始未差分數據
# =====================================================================
df_sales = pd.read_csv("ts_sales.csv")
df_coffee = df_sales[df_sales['product'] == 'coffee_machine'].copy()
df_coffee['date'] = pd.to_datetime(df_coffee['date'])
df_coffee = df_coffee.sort_values('date')

print("=== 開啟『季節性 Auto-SARIMA』自動化搜尋 ===")
print("-" * 60)

# =====================================================================
# 2. 解鎖季節性參數 (全自動尋找 SARIMA 靈魂組合)
# =====================================================================
auto_sarima_model = pm.auto_arima(
    df_coffee['units'],     
    seasonal=True,                # 開啟季節性
    m=7,                          # 核心密碼：指定每週週期為 7 天    
    stepwise=True,                # 啟動智慧步進演算法，避免電腦算到當機
    information_criterion='aic',  # 依舊以 AIC 最小化為唯一裁判
    trace=True                    # 列印出後台高階日誌
)

print("-" * 65)
print("=== 季節性搜尋結束！===")
print(auto_sarima_model.summary())

