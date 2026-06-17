# -*- coding: utf-8 -*-

"""
11-4-1建立流失挽回的ROI模型
"""

import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score, accuracy_score
import numpy as np
import joblib

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

# 1. 載入 11-3-1 存好的優化模型，以xgb為例
model = joblib.load("xgb_model.pkl")

# 取得測試集的預測機率
# predict_proba 會回傳 [不流失機率, 流失機率]，我們取 index 1 代表流失機率
y_prob = model.predict_proba(X_test)[:, 1]

#%%

# 1. 準備模擬數據：結合預測機率與真實月費
# 假設我們已經有了模型預測的流失機率 y_prob

simulation_df = X_test.copy()
simulation_df['Churn_Prob'] = y_prob  # 這是模型給出的流失機率

# 2. 定義商務參數 (這就是假設的「會計思維」)
COUPON_VALUE = 20          # 優惠券金額 (假設每月折抵 20 元，持續 3 個月 = 60 元)
COUPON_MONTHS = 3          # 持續補貼 3 個月
MARKETING_OPEX = 5         # 推播簡訊與行政成本
RECOVERY_RATE = 0.25       # 挽回成功率 (修正：並非 100% 的人拿了券都會留下)
LTV_HORIZON = 6            # 我們看接下來 6 個月的營收貢獻

# 4. 計算損益邏輯
def calculate_profit(row):
    # 成本端（確定發生）
    coupon_cost = COUPON_VALUE * COUPON_MONTHS
    campaign_cost = coupon_cost + MARKETING_OPEX
    
    # 收益端（期望值）
    expected_ltv = row['MonthlyCharges'] * LTV_HORIZON
    expected_revenue = expected_ltv * RECOVERY_RATE
    
    # 淨利潤
    return expected_revenue - campaign_cost

# 執行模擬
simulation_df['ROI_Profit'] = simulation_df.apply(calculate_profit, axis=1)

# 5.總體 ROI
total_profit = simulation_df['ROI_Profit'].sum()
# 有效挽回（正ROI）
profitable_users = simulation_df[simulation_df['ROI_Profit'] > 0]

print("總ROI利潤:", total_profit)
print("可挽回用戶數:", len(profitable_users))
print("平均每人ROI:", simulation_df['ROI_Profit'].mean())
