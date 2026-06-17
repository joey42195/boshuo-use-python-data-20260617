# -*- coding: utf-8 -*-

"""
11-3-4 F1-Score與ROC-AUC
"""

import pandas as pd
import matplotlib.pyplot as plt

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 1. 去除全域警告訊息 (如 XGBoost 的參數過時警告)
import warnings
warnings.filterwarnings('ignore')

# 載入 處理好的資料
df = pd.read_pickle('Telco-Customer-Churn_11-2-3.pkl')
# 特徵很多
df.columns

# 1、核心數值
num_features = [
    'tenure', 
    'MonthlyCharges'
]

# 商業衍生特徵：「行為密度 + 綁定程度」
derived_features = [
    'Avg_Monthly_Benefit',
    'Service_Count'
]

#合約與支付結構
behavior_features = [
    'Contract_encoded',
    'PaperlessBilling',
    'SeniorCitizen'
]

# One-hot 支付方式（保留但精簡）
payment_features = [
    'PaymentMethod_Bank transfer (automatic)',
    'PaymentMethod_Credit card (automatic)',
    'PaymentMethod_Electronic check',
    'PaymentMethod_Mailed check'
]

# 最終 feature list
features = (
    num_features +
    derived_features +
    behavior_features +
    payment_features
)


# 在進入模型訓練前，我們先將資料切分為訓練集與測試集，並保持類別比例一致，以避免評估偏誤。
X = df[features]
y = df['Churn']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

import joblib
model = joblib.load('xgb_model.pkl')

# 1. 取得模型預測的「機率值」 (這是計算 AUC 的核心)
# 我們使用優化後的模型 (model 是你在 11-3-1 最後跑的那一個)
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

#%%
"""
ROC曲線視覺化
"""

from sklearn.metrics import roc_curve, auc
from sklearn.metrics import classification_report, f1_score

f1 = f1_score(y_test, y_pred)

# 2. 計算核心指標
f1 = f1_score(y_test, y_pred)
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

# 3. 輸出指標
print("--- 11-3-4 模型商務戰力報告 ---")
print(f"1. F1-Score (平衡戰力): {f1:.4f}")
print(f"   --> 解釋：在『抓得全』與『不亂抓』之間，模型目前的綜合平衡得分。")
print(f"2. ROC-AUC (排序戰力): {roc_auc:.4f}")
print(f"   --> 解釋：模型有 {roc_auc:.2%} 的機率，能正確辨別誰才是真正的高風險流失者。")
print("-" * 50)

# 4. 繪製 ROC 曲線
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--') # 瞎猜基準線
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('誤報率 (False Positive Rate)')
plt.ylabel('抓取率 (True Positive Rate)')
plt.title('模型戰鬥力地圖 (ROC Curve)')
plt.legend(loc="lower right")
plt.grid(alpha=0.3)

plt.show()








