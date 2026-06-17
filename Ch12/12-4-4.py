# -*- coding: utf-8 -*-

"""
12-4-4模型優化方向—同時使用多項式與對數轉換
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import PolynomialFeatures

import matplotlib.pyplot as plt
import seaborn as sns

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False


# 1. 讀取與準備數據 (一次性處理)
df = pd.read_pickle('diamonds_cleaned.pkl')


#%%

# 多項式 + log

# =============================================================================
#混合優化實作：手動拆解多項式特徵與對數模型
# =============================================================================


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

# 5. 繪圖診斷
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# 左圖：混合優化後的殘差分佈 (應呈現完美的對稱鐘形)
sns.histplot(residuals_log_mixed, kde=True, ax=ax1, color='#e67e22')
ax1.axvline(0, color='red', linestyle='--')
ax1.set_title("12-4-4 混合優化：殘差分佈 (Polynomial + Log)", fontsize=14)

# 右圖：混合優化後的殘差散佈 (檢查彎曲是否消失)
sns.scatterplot(x=y_pred_log_mixed, y=residuals_log_mixed, alpha=0.3, color='#f39c12', ax=ax2)
ax2.axhline(0, color='red', linestyle='--', linewidth=2)
ax2.set_title("12-4-4 混合優化：殘差散佈 (徹底消除系統性規律)", fontsize=14)
ax2.set_xlabel("對數預測價格 (Predicted Log Price)")
ax2.set_ylabel("對數預測誤差")

plt.tight_layout()

plt.show()

print(f"混合模型測試集 R2 Score: {r2_score(y_test_log, y_pred_log_mixed):.4f}")


