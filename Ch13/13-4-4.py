# -*- coding: utf-8 -*-
"""
13-4-4 Auto-ARIMA實戰—讓模型理解商業事件
"""

import pandas as pd
import numpy as np
import pmdarima as pm

# =====================================================================
# 1. 資料讀取與特徵對齊
# =====================================================================
df_sales = pd.read_csv("ts_sales_promot.csv")
df_coffee = df_sales[df_sales['product'] == 'coffee_machine'].copy()
df_coffee['date'] = pd.to_datetime(df_coffee['date'])
df_coffee.set_index('date', inplace=True)
df_coffee = df_coffee.sort_index()

# 跨品類特徵工程：引入膠囊滯後一期銷量
df_capsule = df_sales[df_sales['product'] == 'capsule'].copy()
df_capsule['date'] = pd.to_datetime(df_capsule['date'])
df_capsule.set_index('date', inplace=True)
df_capsule = df_capsule.sort_index()

# 建立外生變數矩陣
df_coffee['capsule_lag1'] = df_capsule['units'].shift(1)
df_coffee = df_coffee.dropna()

# 切出訓練集（扣除最後 7 天）
train_df = df_coffee.iloc[:-7]

y_train = train_df['units']
# 準備好外生變數矩陣
X_train = train_df[['is_coffee_promo', 'capsule_lag1']].astype(float)

# =====================================================================
# 2. 啟動 Auto-ARIMA 自動搜尋
# =====================================================================

full_auto_model = pm.auto_arima(
    y_train, 
    X=X_train,           # 關鍵：這次把外生變數塞給它
    start_p=0, max_p=2,  
    start_q=0, max_q=3,  
    d=None,              
    seasonal=True,       # 開啟季節性
    m=7,                 # 每週 7 天週期
    stepwise=True,       
    information_criterion='aic',  
    trace=True           
)

print("-" * 60)
print("=== 印出報告 ===")
print(full_auto_model.summary())

