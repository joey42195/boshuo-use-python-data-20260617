# -*- coding: utf-8 -*-
"""
11-5-4 SHAP相依圖分析—尋找風險臨界點
"""

import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import shap
import matplotlib.pyplot as plt
import joblib
# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

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


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

#%%

model = joblib.load("xgb_model.pkl")

# 使用 SHAP
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

plt.figure(figsize=(10, 6))

shap.dependence_plot(
    "MonthlyCharges",
    shap_values,
    X_test,
    interaction_index="auto",
    show=False
)
plt.title("11-5-4 MonthlyCharges 相依圖 : 尋找價格臨界點", fontsize=14)
plt.axhline(
    y=0,
    color='r',
    linestyle='--',
    alpha=0.3
)
plt.savefig('11-5-4.png', dpi=300, bbox_inches='tight')
plt.show()