# -*- coding: utf-8 -*-
"""
13-4-2 Auto-ARIMA實戰—自動搜尋不等於自動理解
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

print("=== 啟動 Auto-ARIMA 自動參數搜尋引擎 ===")
print("-" * 60)

# =====================================================================
# 2. 配置自動搜尋超參數
# =====================================================================
# auto_arima 會自動幫我們測試平穩性 (決定 d)，並遍歷 p 與 q 的組合
auto_model = pm.auto_arima(
    df_coffee['units'], 
    start_p=0, max_p=2,   # 設定 自迴歸 (p) 的搜尋範圍
    start_q=0, max_q=3,  # 設定 移動平均 (q) 的搜尋範圍
    d=None,      # 設為 None讓演算法自動決定最佳差分次數
    seasonal=False,   # 本節先聚焦常規 ARIMA，暫時關閉季節性
    stepwise=True,  # 啟動「步進演算法」，能大幅縮短搜尋時間
    information_criterion='aic',  #指定用 AIC 分數最小的
    trace=True      #  過程列印出來
)

print("-" * 60)
print("=== 自動搜尋結束！ ===")
print(auto_model.summary()) 
