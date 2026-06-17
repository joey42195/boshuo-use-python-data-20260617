# -*- coding: utf-8 -*-

"""
11-3-1特徵選擇與基準模型建立
"""

import pandas as pd

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

# XGBoost 模型
from xgboost import XGBClassifier

xgb_model = XGBClassifier(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric='logloss',
    random_state=42,
    verbosity=0
)

xgb_model.fit(X_train, y_train)

# LightGBM 模型
from lightgbm import LGBMClassifier

lgb_model = LGBMClassifier(
    n_estimators=200,
    learning_rate=0.05,
    num_leaves=31,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    verbosity=-1
)

lgb_model.fit(X_train, y_train)



from sklearn.metrics import accuracy_score, recall_score, precision_score, roc_auc_score

def evaluate(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "auc": roc_auc_score(y_test, y_prob)
    }

xgb_result = evaluate(xgb_model, X_test, y_test)
lgb_result = evaluate(lgb_model, X_test, y_test)

# 整理成對照表
result_df = pd.DataFrame({
    "模型": ["XGBoost", "LightGBM"],
    "Accuracy": [xgb_result["accuracy"], lgb_result["accuracy"]],
    "Precision": [xgb_result["precision"], lgb_result["precision"]],
    "Recall": [xgb_result["recall"], lgb_result["recall"]],
    "AUC": [xgb_result["auc"], lgb_result["auc"]]
})

# 美化顯示（四捨五入）
result_df = result_df.round(4)

print(result_df)


# 2. 模型儲存
# 供 11-3-4 F1-Score與ROC-AUC 使用
import joblib
joblib.dump(xgb_model, 'xgb_model.pkl')
joblib.dump(lgb_model, 'lgb_model.pkl')








