# -*- coding: utf-8 -*-

"""
12-5-1溢價分析—從殘差中尋找市場錯價機會
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

# 2. 篩選：找出「被低估」的前 10 顆鑽石
# 邏輯：殘差越小（負值越大），代表實際價格遠低於模型估算的市場行情。
# 這在商務上代表「CP 值極高」，是採購的首選。
bargains = analysis_df.sort_values(by='Residual').head(10)

print("--- 12-5-1 採購優先建議清單 (市場低估件) ---")
# 為了閱讀方便，將結果格式化
pd.options.display.float_format = '{:.2f}'.format
print(bargains[['carat', 'cut', 'Actual_Price', 'Predicted_Price', 'Residual']])

# 3. 篩選：找出「被高估」的前 10 顆鑽石 (回頭看 17803 那種情況)
# 邏輯：殘差越大（正值越大），代表模型認為它沒那麼貴，實際卻賣很貴，可能是品牌溢價或數據未捕捉的瑕疵。
overpriced = analysis_df.sort_values(by='Residual', ascending=False).head(10)

print("\n--- 12-5-1 採購避雷清單 (市場溢價件) ---")
print(overpriced[['carat', 'cut', 'Actual_Price', 'Predicted_Price', 'Residual']])

