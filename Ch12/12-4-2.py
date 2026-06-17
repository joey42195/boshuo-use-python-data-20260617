# -*- coding: utf-8 -*-

"""
12-4-2模型優化方向—使用多項式迴歸
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


import matplotlib.pyplot as plt
import seaborn as sns

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False


# 1. 讀取 11-2 封裝好的精煉數據
df = pd.read_pickle('diamonds_cleaned.pkl')

# 2. 準備特徵矩陣 (X) 與 目標向量 (y)
X = df.drop('price', axis=1)  # 特徵：carat, cut, color, clarity, depth, table
y = df['price']               # 目標：美金定價
X.columns

# 3. 執行拆分 (80/20 法則)
# random_state=42 確保實驗的可重複性，讓每次訓練的「起跑線」一致
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#%%

# 1. 初始化線性回歸模型
model = LinearRegression()


#%%

# =============================================================================
# 11-4-2 優化：引入多項式特徵（Polynomial Transformation）
# =============================================================================
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# 建立 PolynomialFeatures 物件
poly = PolynomialFeatures(
    degree=2,        # 產生「二次項」(例如 x^2, x*y)
    include_bias=False  # 不加入常數項 (1)，避免和模型的 intercept 重複
)

# 專業做法：在訓練集 fit，在測試集 transform
# 處理訓練集  模型可以學：線性關係（carat）, 非線性關係（carat²）
carat_train_poly = poly.fit_transform(X_train[['carat']]) # 這一步會「學到」轉換規則（例如產生平方項）
X_train_poly = X_train.drop(columns=['carat']).copy() # 複製一份資料（避免改到原始 X_train）


X_train_poly['carat'] = carat_train_poly[:, 0]   # poly 產生的第 0 欄 = 原始 carat
X_train_poly['carat_squared'] = carat_train_poly[:, 1]  # poly 產生的第 1 欄 = carat^2（平方項）

# 處理測試集 (絕對不要在測試集 fit)
carat_test_poly = poly.transform(X_test[['carat']])  # 因為測試集不能參與「學習過程」
X_test_poly = X_test.drop(columns=['carat']).copy()

X_test_poly['carat'] = carat_test_poly[:, 0]   # 保持和訓練集完全一樣的欄位結構
X_test_poly['carat_squared'] = carat_test_poly[:, 1]


print(f"原始特徵數量: {X_train.shape[1]}")
print(f"多項式擴張後特徵數量: {X_train_poly.shape[1]} (已具備捕捉曲線的能力)")

# 2. 步驟二：模型訓練 (Model Training)
# 使用擴張後的特徵矩陣來擬合線性回歸引擎
poly_model_manual = LinearRegression()
poly_model_manual.fit(X_train_poly, y_train)

# 3. 步驟三：執行預測與計算殘差
y_pred_poly = poly_model_manual.predict(X_test_poly)
res_poly = y_test - y_pred_poly

print(f"殘差平均值: {res_poly.mean():.2f}")

# 繪圖
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

sns.histplot(res_poly, kde=True, ax=ax1, color='#27ae60')
ax1.axvline(0, color='red', linestyle='--')
ax1.set_title("優化後：殘差分佈（趨於對稱常態）")

sns.scatterplot(x=y_pred_poly, y=res_poly, alpha=0.3, ax=ax2, color='#2ecc71')
ax2.axhline(0, color='red', linestyle='--')
ax2.set_title("優化後：殘差散佈（漏斗收斂，彎曲消失）")
plt.tight_layout()
plt.show()

print(f"優化後測試集 R2: {poly_model_manual.score(X_test_poly, y_test):.4f}")

#%%
