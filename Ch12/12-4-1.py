# -*- coding: utf-8 -*-

"""
12-4-1殘差分佈圖—檢查誤差是否符合常態分佈
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

# 2. 訓練模型 (Fit)
model.fit(X_train, y_train)

# 3. 執行預測 (Predict)
# 利用訓練好的「定價公式」，分別算出模型對『已知數據』與『未知數據』的出價建議。
y_train_pred = model.predict(X_train) # 評估模型在學習樣本上的擬合程度
y_test_pred = model.predict(X_test)   # 驗證模型對陌生鑽石的預測能力 (模擬未來市場)


# =============================================================================
# 11-4-1 殘差分析：診斷定價是否存在「系統性偏見」
# =============================================================================

# 1. 計算殘差 (Residuals)
# 殘差 = 真實市場價格 - 模型預測價格
# 正值代表模型「低估」了鑽石，負值代表模型「高估」了鑽石
residuals = y_test - y_test_pred
print(f"殘差平均值: {residuals.mean():.2f}")

# 2. 繪製殘差分佈圖
plt.figure(figsize=(8, 5))
sns.histplot(residuals, kde=True)

# 3. 加上診斷輔助線：理想情況下，殘差應以 0 為中心呈現常態分佈
plt.axvline(0, color='red', linestyle='--', label='理想零誤差線')

plt.title("12-4-1 殘差分佈圖：診斷系統性偏見", fontsize=14)
plt.xlabel("預測誤差 (真實價格 - 預測價格)", fontsize=12)
plt.ylabel("頻率 (次數)", fontsize=12)
plt.legend()
# plt.savefig('11-4-1.png', dpi=300, bbox_inches='tight')
plt.show()

plt.figure(figsize=(10, 6))

# 散佈圖：X 軸為模型給出的建議價，Y 軸為與現實的落差
sns.scatterplot(x=y_test_pred, y=residuals, alpha=0.4, color='#3498db')

# 畫出 Y=0 的基準線，這是我們追求的「精準定價」
plt.axhline(0, color='red', linestyle='--', linewidth=2, label='零誤差線')

plt.title("12-4-1 殘差散佈圖：檢視異質變異性", fontsize=14)
plt.xlabel("模型預測價格 (Predicted Price)", fontsize=12)
plt.ylabel("預測誤差 (Residuals)", fontsize=12)
plt.legend()
plt.show()

