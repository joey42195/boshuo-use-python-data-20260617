# -*- coding: utf-8 -*-

"""
12-3-2 係數的商業意義—從參數到決策規則
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


# 1. 讀取封裝好的數據
# 使用 pickle 能確保我們辛苦轉換的 Ordinal Encoding 等級（1-8）不會變回字串
df = pd.read_pickle('diamonds_cleaned.pkl')

# 2. 準備特徵矩陣 (X) 與 目標向量 (y)
# 我們捨棄了 x, y, z，因為它們與重量高度重疊（共線性）
X = df.drop('price', axis=1)  # 特徵：carat, cut, color, clarity, depth, table
y = df['price']               # 目標：美金定價

# 3. 執行拆分 (80/20 法則)
# random_state=42 確保實驗的可重複性，讓每次訓練的「起跑線」一致
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"訓練樣本: {len(X_train)} (這是模型學習『定價邏輯』的教科書)")
print(f"測試樣本: {len(X_test)} (這是模擬『未來市場』的期末考題)\n")

# 4. 初始化線性回歸模型
# 線性回歸是商業解釋力最強的模型，能讓我們清楚看見每一分錢的來源
model = LinearRegression()

# 5. 訓練模型：尋找特徵與價格之間的最優線性關係
model.fit(X_train, y_train)



#%%

# =============================================================================
# 係數解讀：每多一克拉，價格會增加多少？
# =============================================================================

coef_df = pd.DataFrame({'Feature': X.columns, 'Coefficient': model.coef_})
print(coef_df.sort_values(by='Coefficient', ascending=False))

