# -*- coding: utf-8 -*-

"""
12-4-5穩健性檢驗—K-Fold交叉驗證
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import cross_val_score, KFold

import matplotlib.pyplot as plt
import seaborn as sns

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False


# 1. 讀取與準備數據 (一次性處理)
df = pd.read_pickle('diamonds_cleaned.pkl')


# 1. 準備數據：對目標變數 y 進行 Log 轉換 (解決 image_70ddc5.png 的漏斗問題)
X = df.drop('price', axis=1)
y_log = np.log1p(df['price'])


# =============================================================================
# 穩健性檢驗：K-Fold 交叉驗證 (確保模型不是過度擬合)
# =============================================================================
from sklearn.model_selection import cross_val_score, KFold

# 1. 準備數據：對全體數據進行 Log 與多項式轉換
# 注意：在 CV 中，我們通常對「全體 X」進行轉換，或者使用迭代器手動轉換
poly_trans_full = PolynomialFeatures(degree=2, include_bias=False)
X_poly_full = poly_trans_full.fit_transform(X) # X 為全體特徵數據

# 2. 定義 K-Fold 策略 (建議 5 到 10 折)
# shuffle=True 確保數據順序被打亂，避免批次性的鑽石數據干擾結果
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# 3. 執行交叉驗證
# 我們觀察 R2 的穩定性。如果各折分數相近，代表模型非常穩健。
cv_r2_scores = cross_val_score(LinearRegression(), X_poly_full, y_log, cv=kf, scoring='r2')

print(f"--- 11-6-3 交叉驗證報告 ---")
print(f"各折 R2 分數: {cv_r2_scores}")
print(f"平均 R2 分數: {cv_r2_scores.mean():.4f}")
print(f"R2 標準差 (變異度): {cv_r2_scores.std():.4f}")

# 4. 商務解讀：如果標準差極低 (e.g., < 0.005)
# 代表這套「多項式 + 對數」定價系統不論遇到哪一批數據，準確度都極其穩定。




