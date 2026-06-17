# -*- coding: utf-8 -*-

"""
11-5-1交叉驗證
"""


import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score, accuracy_score
import numpy as np
import joblib

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

#%%

ratio = len(y_train[y_train == 0]) / len(y_train[y_train == 1])

# 1. 初始化交叉驗證器（5-Fold）
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# 2. 定義模型（使用加權 XGBoost）
cv_model = XGBClassifier(
    n_estimators=100,
    scale_pos_weight=ratio,  # 處理類別不平衡
    random_state=42,
    eval_metric='logloss'
)

# 3. 執行交叉驗證（使用 ROC-AUC 作為評估指標）
cv_scores = cross_val_score(
    cv_model,
    X_train,
    y_train,
    cv=skf,
    scoring='roc_auc'
)

# 4. 輸出結果
print(f"5 折交叉驗證 AUC 分數: {cv_scores}")
print(f"平均 AUC 分數 (Mean): {cv_scores.mean():.4f}")
print(f"分數標準差 (Std): {cv_scores.std():.4f}")

