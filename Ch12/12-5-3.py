# -*- coding: utf-8 -*-

"""
12-5-3模擬情境—市場結構變動下的庫存價值重估
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
# 12-5-3 商務模擬：當市場克拉單價權重調升 10% 的庫存價值變動
# =============================================================================
import copy

# 1. 複製一份原本的模型，避免影響到原始定價引擎
simulation_model = copy.deepcopy(mixed_model_manual)

# 2. 找出 'carat' 在多項式特徵中的位置
# 因為我們手動拆解了 PolynomialFeatures，所以需要找出對應的索引
feature_names = poly_trans.get_feature_names_out(X.columns)
carat_idx = list(feature_names).index('carat')

# 3. 執行模擬：將 carat 的係數調升 10%
# 這裡修改的是線性回歸中的 coef_ (斜率)
original_coef = simulation_model.coef_[carat_idx]
simulation_model.coef_[carat_idx] = original_coef * 1.10

print(f"--- 12-5-3 模擬參數調整 ---")
print(f"Carat 原始係數: {original_coef:.4f}")
print(f"Carat 模擬係數: {simulation_model.coef_[carat_idx]:.4f} (調升 10%)")

# 4. 進行全庫存重估 (以 X_test 為例模擬現有庫存)
# A. 原始模型預估總價值
y_pred_original = np.expm1(mixed_model_manual.predict(X_test_poly))
total_value_current = np.sum(y_pred_original)

# B. 模擬模型預估總價值
y_pred_simulated = np.expm1(simulation_model.predict(X_test_poly))
total_value_simulated = np.sum(y_pred_simulated)

# 5. 計算財務影響
value_diff = total_value_simulated - total_value_current
growth_rate = (value_diff / total_value_current) * 100

print(f"\n--- 12-5-3 財務壓力測試結果 ---")
print(f"現有庫存估計總值: ${total_value_current:,.0f}")
print(f"模擬重估後總價值: ${total_value_simulated:,.0f}")
print(f"預期價值變動金額: ${value_diff:,.0f}")
print(f"庫存增值幅度: {growth_rate:.2f}%")




#%%

"""
補充
"""

# 2. 計算商務核心指標 (真實尺度)
mae = mean_absolute_error(y_test_original, y_pred_original_mixed)
rmse = np.sqrt(mean_squared_error(y_test_original, y_pred_original_mixed))
final_r2 = r2_score(y_test_original, y_pred_original_mixed)

print(f"--- 混合優化模型 最終商務指標 ---")
print(f"平均絕對誤差 (MAE): ${mae:.2f} (平均每顆鑽石預測誤差約為 {mae:.2f} 美金)")
print(f"均方根誤差 (RMSE): ${rmse:.2f}")
print(f"最終決定係數 (R2): {final_r2:.4f}")

# 3. 觀察前 10 筆真實與預測的對照表
check_df = pd.DataFrame({
    '實際美金價格': y_test_original,
    '模型預測價格': y_pred_original_mixed,
    '美金誤差': y_test_original - y_pred_original_mixed
})

print("\n前 10 筆預測結果檢驗：")
print(check_df.head(10).round(2))

#%%



