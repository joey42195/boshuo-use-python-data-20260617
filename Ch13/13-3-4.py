# -*- coding: utf-8 -*-

"""
13-3-4 建立SARIMAX模型
"""

#%%

# 耗材連帶外生變數 SARIMAX 實戰

import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX

# =====================================================================
# 1. 數據結構轉換與「膠囊 Lag 1」特徵工程
# =====================================================================
# df_sales = pd.read_csv("ts_sales_capsule.csv")
df_sales = pd.read_csv("ts_sales.csv")
df_sales['date'] = pd.to_datetime(df_sales['date'])
df_sales = df_sales.sort_values('date')

# 長表 → 寬表（產品並列）
df_wide = df_sales.pivot(index='date', columns='product', values='units')

df_market = df_wide.sort_index()

# 外生變數：膠囊 Lag 1
df_market['capsule_lag1'] = df_market['capsule'].shift(1)

# 去除 NaN（時間序列第一筆）
df_market = df_market.dropna()

print("=== SARIMAX（單一外生變數：capsule_lag1）===")
print(df_market[['coffee_machine', 'capsule_lag1']].tail(3))
print("-" * 60)

# =====================================================================
# 2. 定義切分點：用前 358 天訓練，留最後 7 天當作測試
# 為評估模型泛化能力，將資料分為訓練集與測試集：
# 訓練集：前期歷史資料（用於模型估計）
# 測試集：最後 7 天（用於模擬實際預測場景）
# =====================================================================
train_df = df_market.iloc[:-7]
test_df = df_market.iloc[-7:]

# 目標變數 Y：咖啡機銷量
y_train = train_df['coffee_machine']

# 外生變數 X：【昨天的膠囊銷量】
X_train = train_df[['capsule_lag1']]

# =====================================================================
# 3.  SARIMAX(0,1,1)x(0,1,1)7 模型
# =====================================================================
from statsmodels.tsa.statespace.sarimax import SARIMAX
model_final = SARIMAX(
    y_train,
    order=(0, 1, 1),
    seasonal_order=(0, 1, 1, 7),
    exog=X_train  
)
results = model_final.fit()

# =====================================================================
# 4. 建立未來外生變數（capsule_lag1），並預測
#    注意：這裡用 test 的 lag 當作模擬已知資訊
# =====================================================================

future_exog = pd.DataFrame({
    'capsule_lag1': test_df['capsule'].shift(1).values
}, index=test_df.index)

# 第一筆 shift 仍可能 NaN → 用前值補
# future_exog = future_exog.fillna(method='bfill')
future_exog = future_exog.bfill()
forecast = results.forecast(steps=7, exog=future_exog)


# =====================================================================
# 5. 報表輸出
# =====================================================================
df_report = pd.DataFrame({
    '預測日期': test_df.index.strftime('%Y-%m-%d'),
    '膠囊引力參考(昨日)': np.round(future_exog['capsule_lag1'], 1),
    '預估主機銷量(台)': np.round(forecast.values, 1),
    '實際主機銷量(台)': np.round(test_df['coffee_machine'].values, 1)
})

print("=== SARIMAX（單外生變數版本）預測結果 ===")
print(df_report.to_string(index=False))












