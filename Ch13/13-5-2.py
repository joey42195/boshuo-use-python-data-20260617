# -*- coding: utf-8 -*-
"""
13-5-2 利用模型預測未來
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm

# =====================================================================
# 1. 載入全量資料 (不再保留最後 7 天，365天全部投入訓練)
# =====================================================================
df_sales = pd.read_csv("ts_sales_promot.csv")

df_coffee = df_sales[df_sales['product'] == 'coffee_machine'].copy()
df_coffee['date'] = pd.to_datetime(df_coffee['date'])
df_coffee.set_index('date', inplace=True)
df_coffee = df_coffee.sort_index()

df_capsule = df_sales[df_sales['product'] == 'capsule'].copy()
df_capsule['date'] = pd.to_datetime(df_capsule['date'])
df_capsule.set_index('date', inplace=True)
df_capsule = df_capsule.sort_index()

# 特徵工程：全量對齊昨天的膠囊銷量
df_coffee['capsule_lag1'] = df_capsule['units'].shift(1)
df_coffee = df_coffee.dropna() # 這時我們擁有最完整的歷史軌跡

# =====================================================================
# 2. 定義全量訓練集 (Full Dataset)
# =====================================================================
y_full = df_coffee['units']
X_full = df_coffee[['is_coffee_promo', 'capsule_lag1']].astype(float)

# =====================================================================
# 3. 滿載擬合：讓模型使用到所有的資料
# =====================================================================
production_model = sm.tsa.statespace.SARIMAX(
    y_full,
    exog=X_full,
    order=(0, 1, 1),              # 使用 auto_arima 的參數
    seasonal_order=(2, 0, 1, 7),   
    enforce_stationarity=False,
    enforce_invertibility=False
)
production_results = production_model.fit(disp=False)

# =====================================================================
# 4. 關鍵核心：手動編織未來 7 天的行銷戰略劇本 (X_future)
# =====================================================================
# 假設今天是 2025-12-31，我們要預報 2026-01-01 ~ 2026-01-07
future_dates = pd.date_range(start="2026-01-01", periods=7, freq='D')

# 行銷總監給出的未來劇本：預計在元旦連假 (週四到週六) 發動新一波主機降價！
future_promo = [1, 1, 1, 0, 0, 0, 0]  

# 跨品類引力：昨天的膠囊實際銷量。
# 注意：第一天的昨天也就是 12-31（已知），
# 後續 6 天在實務上可用膠囊模型同步預測值替換，
# 此處用歷史最後幾天模擬
future_capsule_lag1 = [185.0, 190.0, 175.0, 120.0, 115.0, 110.0, 112.0] 
# # 膠囊模型產生的 Mean 預測，見下一小節
# future_capsule_lag1 = [174.9, 181.6, 156.3, 118.1, 95.8, 106.1, 141.0]

X_future = pd.DataFrame({
    'is_coffee_promo': future_promo,
    'capsule_lag1': future_capsule_lag1
}, index=future_dates)

# =====================================================================
# 5. 向未來預測：提取預報中軸與 95% 預測區間
# =====================================================================
forecast_future = production_results.get_forecast(steps=7, exog=X_future)
forecast_future_df = forecast_future.summary_frame(alpha=0.05)

# =====================================================================
# 6. 格式化輸出
# =====================================================================
future_report = pd.DataFrame(index=future_dates)
future_report['預報日期'] = future_dates.strftime('%Y-%m-%d')
future_report['營運狀態'] = X_future['is_coffee_promo'].apply(lambda x: '元旦大促' if x==1 else '常規營運')

# 風控籌碼格式化
future_report['備貨下界 (Lower PI)'] = np.round(forecast_future_df['mean_ci_lower'].values, 1)
future_report['預估銷售 (Mean)'] = np.round(forecast_future_df['mean'].values, 1)
future_report['備貨上界 (Upper PI)'] = np.round(forecast_future_df['mean_ci_upper'].values, 1)

print("\n" + "===" * 25)
print("未來 7 天生產備貨戰略報表")
print("===" * 25)
print(future_report.to_string(index=False))



