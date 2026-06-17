# -*- coding: utf-8 -*-

"""
11-5-2超參數調優
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


from sklearn.model_selection import RandomizedSearchCV

# 1. 將比例也納入搜索空間
# 我們在 2.77 (ratio) 的上下進行微調測試
param_dist = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 4, 5],
    'learning_rate': [0.01, 0.05, 0.1],
    'subsample': [0.8, 0.9],
    'colsample_bytree': [0.8, 0.9],
    # 這裡加入比例的變動空間，從 2.5 到 3.0 之間搜索
    'scale_pos_weight': [ratio * 0.9, ratio, ratio * 1.1] 
}

# 2. 執行搜索
random_search = RandomizedSearchCV(
    estimator=XGBClassifier(eval_metric='logloss', random_state=42),
    param_distributions=param_dist,
    n_iter=15,          # 增加嘗試次數
    scoring='roc_auc',  # 依然以排序能力為準
    cv=skf, 
    verbose=1,
    n_jobs=-1,
    random_state=42
)

print("--- 11-5-2 全方位超參數調優 (含比例權重) ---")
random_search.fit(X_train, y_train)

# 3. 獲取最佳參數
best_params = random_search.best_params_
print(f"最佳參數組合：{best_params}")

# 4. 用這組最強參數重新做一次 business_eval
final_best_model = random_search.best_estimator_
y_pred_final = final_best_model.predict(X_test)

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

xgb_result = evaluate(final_best_model, X_test, y_test)
print("=== XGBoost 模型效能評估 ===")
print(f"Accuracy : {xgb_result['accuracy']:.4f}")
print(f"Recall   : {xgb_result['recall']:.4f}")
print(f"Precision: {xgb_result['precision']:.4f}")
print(f"AUC      : {xgb_result['auc']:.4f}")

# print("\n最終優化模型評估：")
# business_eval(y_test, y_pred_final)



