# -*- coding: utf-8 -*-

"""
12-5-2區間估計—從單點預測到風險定價
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error, mean_squared_error

# 1. 讀取與準備數據 (一次性處理)
df = pd.read_pickle('diamonds_cleaned.pkl')

# 1. 準備數據：對目標變數 y 進行 Log 轉換 (解決 image_70ddc5.png 的漏斗問題)
X = df.drop('price', axis=1)
y_log = np.log1p(df['price'])

X_train, X_test, y_train_log, y_test_log = train_test_split(
    X, y_log, test_size=0.2, random_state=42
)

# 2. 步驟一：手動進行特徵多項式轉換 (解決 image_4aa2d8.png 的彎曲問題)
# 設定 degree=2 包含平方項與交互項
poly_trans = PolynomialFeatures(degree=2, include_bias=False)

# 將訓練集與測試集轉換為多項式維度
X_train_poly = poly_trans.fit_transform(X_train)
X_test_poly = poly_trans.transform(X_test)

# 3. 步驟二：手動訓練線性回歸模型
# 此模型現在是在「多項式特徵」上預測「對數價格」
mixed_model_manual = LinearRegression()
mixed_model_manual.fit(X_train_poly, y_train_log)

# 4. 預測與計算殘差
y_pred_log_mixed = mixed_model_manual.predict(X_test_poly)
residuals_log_mixed = y_test_log - y_pred_log_mixed


# 1. 執行反轉對數轉換 (將 Log 尺度轉回美金尺度)
# 必須先還原，後續的 MAE 與 RMSE 才有商業意義
y_test_original = np.expm1(y_test_log)
y_pred_original_mixed = np.expm1(y_pred_log_mixed)

#%%

# =============================================================================
# 12-5-1 採購決策支援：從預測誤差中尋找「漏網之魚」
# =============================================================================

# 1. 建立分析用的 DataFrame，整合特徵與優化後的預測結果
# 注意：這裡使用我們剛還原的 y_test_original 與 y_pred_original_mixed
analysis_df = X_test.copy()
analysis_df['Actual_Price'] = y_test_original.values
analysis_df['Predicted_Price'] = y_pred_original_mixed
analysis_df['Residual'] = analysis_df['Actual_Price'] - analysis_df['Predicted_Price']



#%%

# =============================================================================
# 12-5-2 區間估計：產出具備議價緩衝帶的預測清單
# =============================================================================

# 1. 計算對數空間下的殘差標準差 (Standard Deviation of Residuals)
# 這是衡量模型「平均手感誤差」的指標
std_error_log = np.std(residuals_log_mixed)

# 2. 設定信心水準 (95% 信心區間約為正負 1.96 倍標準差)
confidence_factor = 1.96

# 3. 在對數空間計算上限與下限
analysis_df['Log_Lower'] = y_pred_log_mixed - (confidence_factor * std_error_log)
analysis_df['Log_Upper'] = y_pred_log_mixed + (confidence_factor * std_error_log)

# 4. 將區間還原為真實美金尺度 (np.expm1)
analysis_df['Price_Lower'] = np.expm1(analysis_df['Log_Lower'])
analysis_df['Price_Upper'] = np.expm1(analysis_df['Log_Upper'])

# 5. 整理最終商務清單
# 我們挑選幾筆案例，看看「議價緩衝帶」如何呈現
pricing_guide = analysis_df[['carat', 'cut', 'Actual_Price', 'Predicted_Price', 'Price_Lower', 'Price_Upper']].head(10)

print("--- 12-5-2 鑽石定價議價指南 (95% 預測區間) ---")
pd.options.display.float_format = '{:.2f}'.format
print(pricing_guide)

