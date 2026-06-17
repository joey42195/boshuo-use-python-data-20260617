# -*- coding: utf-8 -*-

"""
13-3-2 建立ARIMA模型
"""
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

# =====================================================================
# 1. 資料載入與前處理 (確保時間序列連續性)
# =====================================================================
# 直接讀取原始未差分的 CSV 檔案，將差分完全交給模型內建機制
df_sales = pd.read_csv("ts_sales.csv")

# 篩選核心目標產品：咖啡機
df_coffee = df_sales[df_sales['product'] == 'coffee_machine'].copy()

# 將日期欄位轉換為時間格式，並由遠至近嚴格排序，這是時間序列建模的鐵律
df_coffee['date'] = pd.to_datetime(df_coffee['date'])
df_coffee = df_coffee.sort_values('date')

# =====================================================================
# 2. 建立與擬合 ARIMA(0,1,1) 模型 
# =====================================================================

# 取前 360 天的資料作為模型擬合的基礎（訓練集）
training_days = 360
df_train = df_coffee.iloc[:training_days].copy()

# 取最後 5 天的資料作為真實市場對照（測試集）
df_real_test = df_coffee.iloc[training_days:].copy()

# 建立與擬合 ARIMA(0,1,1) 模型 (完全交由內建機制進行自動一階差分與逆差分還原)
model = ARIMA(df_train['units'], order=(0, 1, 1))
model_fit = model.fit()

# =====================================================================
# 3. 未來 5 天預測與商務指標轉換
# =====================================================================
# 設定預測跨度為 5 天，此時模型會基於第 360 天的狀態，向外延伸預測 5 天
forecast_steps = len(df_real_test)
forecast_units = model_fit.forecast(steps=forecast_steps)

# =====================================================================
# 4. 產出預測與真實銷量之對比報表
# =====================================================================
# 封裝對比 DataFrame
df_val_report = pd.DataFrame({
    '預測日期': df_real_test['date'].dt.strftime('%Y-%m-%d').values,
    '實際銷量 (台)': np.round(df_real_test['units'].values, 1),
    '預估銷量 (台)': np.round(forecast_units.values, 1)
})
print(df_val_report)
