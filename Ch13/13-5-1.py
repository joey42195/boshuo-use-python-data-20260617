# -*- coding: utf-8 -*-
"""
13-5-1 信心區間與預測區間的本質差異
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm

# =====================================================================
# 1. 資料前處理與特徵對齊 (建立跨品類膠囊滯後特徵)
# =====================================================================
df_sales = pd.read_csv("ts_sales_promot.csv")

# 主機資料
df_coffee = df_sales[df_sales['product'] == 'coffee_machine'].copy()
df_coffee['date'] = pd.to_datetime(df_coffee['date'])
df_coffee.set_index('date', inplace=True)
df_coffee = df_coffee.sort_index()

# 膠囊資料
df_capsule = df_sales[df_sales['product'] == 'capsule'].copy()
df_capsule['date'] = pd.to_datetime(df_capsule['date'])
df_capsule.set_index('date', inplace=True)
df_capsule = df_capsule.sort_index()

# 特徵工程：將昨天的膠囊銷量做為今天主機的外生推力
df_coffee['capsule_lag1'] = df_capsule['units'].shift(1)
df_coffee = df_coffee.dropna()

# =====================================================================
# 2. 切分訓練集與測試集 (保留最後 7 天作為盲測考卷)
# =====================================================================
train_df = df_coffee.iloc[:-7]
test_df = df_coffee.iloc[-7:]

exog_cols = ['is_coffee_promo', 'capsule_lag1']
X_train = train_df[exog_cols].astype(float)
X_test = test_df[exog_cols].astype(float)

y_train = train_df['units']
y_test = test_df['units']

# =====================================================================
# 3. 配置完全體 SARIMAX 模型並進行擬合
# =====================================================================
# 手動鎖定 auto_arima 幫我們算出的黃金客觀參數 (0,1,1)x(2,0,1)[7]
final_model = sm.tsa.statespace.SARIMAX(
    y_train,
    exog=X_train,
    order=(0, 1, 1),              
    seasonal_order=(2, 0, 1, 7),   
    enforce_stationarity=False,
    enforce_invertibility=False
)
results = final_model.fit(disp=False)

# =====================================================================
# 4. 關鍵核心：提取預測值與 95% 預測區間 (Prediction Interval)
# =====================================================================
# steps=7 代表預測未來 7 天，並傳入未來 7 天的行銷劇本外生變數
forecast_object = results.get_forecast(steps=7, exog=X_test)

# alpha=0.05 代表 95% 的顯著水準，這會幫我們算好 Upper / Lower Bound
forecast_df = forecast_object.summary_frame(alpha=0.05)

# =====================================================================
# 5. 格式化輸出：建立商務風控對齊報表
# =====================================================================
report_df = pd.DataFrame(index=test_df.index)
report_df['預測日期'] = test_df.index.strftime('%Y-%m-%d')

report_df['主機活動狀態'] = test_df['is_coffee_promo'].apply(lambda x: '標記活動' if x==1 else '常規營運')

# 數據對齊（四捨五入至小數點後第一位）
report_df['下界 (Lower PI)'] = np.round(forecast_df['mean_ci_lower'].values, 1)
report_df['預估銷量 (Mean)'] = np.round(forecast_df['mean'].values, 1)
report_df['上界 (Upper PI)'] = np.round(forecast_df['mean_ci_upper'].values, 1)
report_df['實際銷量'] = np.round(y_test.values, 1)
report_df['單點絕對誤差'] = np.round(np.abs(report_df['預估銷量 (Mean)'] - report_df['實際銷量']), 1)

print("\n" + "===" * 25)
print("SARIMAX 報表 (含 95% 預測區間)")
print("===" * 25)
print(report_df.to_string(index=False))
