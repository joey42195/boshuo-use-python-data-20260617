# -*- coding: utf-8 -*-

"""
12-4-3 模型優化方向—使用log對數轉換
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

# =============================================================================
# 引入log特徵（log Transformation）
# =============================================================================

# 1. 讀取與準備數據 (一次性處理)
df = pd.read_pickle('diamonds_cleaned.pkl')
X = df.drop('price', axis=1)
y_log = np.log1p(df['price'])  # 直接對目標進行 Log 轉換

# 2. 執行拆分
X_train, X_test, y_train_log, y_test_log = train_test_split(
    X, y_log, test_size=0.2, random_state=42
)

# 3. 訓練模型
log_model = LinearRegression().fit(X_train, y_train_log)

# 4. 預測與計算對數殘差 (用於診斷模型體質)
y_test_log_pred = log_model.predict(X_test)
residuals_log = y_test_log - y_test_log_pred

# 5. [還原數值] 用於商業報表 (若需要顯示具體美金誤差可使用)
y_test_pred_original = np.expm1(y_test_log_pred)
y_test_original = np.expm1(y_test_log)
residuals_usd = y_test_original - y_test_pred_original # 真實美金誤差
print(residuals_usd)

# 6. 繪製診斷圖
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# 左圖：觀察殘差是否符合常態分佈
sns.histplot(residuals_log, kde=True, ax=ax1, color='#8e44ad')
ax1.axvline(0, color='red', linestyle='--') # 補上一條紅線更專業
ax1.set_title("12-4-3 對數優化後：殘差分佈 (Log Scale)")

# 右圖：觀察漏斗效應是否消失
sns.scatterplot(x=y_test_log_pred, y=residuals_log, alpha=0.3, color='#9b59b6', ax=ax2)
ax2.axhline(0, color='red', linestyle='--')
ax2.set_title("12-4-3 對數優化後：殘差散佈 (消除漏斗效應)")
ax2.set_xlabel("對數預測值 (Predicted Log Price)")
ax2.set_ylabel("對數殘差 (Log Residuals)")

plt.tight_layout()

plt.show()

