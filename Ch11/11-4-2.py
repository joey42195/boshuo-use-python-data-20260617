# -*- coding: utf-8 -*-

"""
11-4-2挽回機率的變動敏感度分析
"""

import pandas as pd
import matplotlib.pyplot as plt

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

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

#%%

# 11-4-2 挽回機率（Recovery Rate）的變動敏感度分析

# 1、遞減型成長
def simulate_recovery_rate(coupon):
    return 0.5 * (1 - np.exp(-0.05 * coupon))

# 2. 建立折扣測試區間
coupons = np.arange(5, 55, 5) # 測試 5, 10, 15... 到 50 元
results = []

# 3. 定義反應函數：模擬coupon與利潤的關係
def calculate_profit(row, coupon):

    # 成本端
    coupon_cost = coupon * COUPON_MONTHS
    campaign_cost = coupon_cost + MARKETING_OPEX

    # 挽回率（跟 coupon 綁定）
    recovery_rate = simulate_recovery_rate(coupon)

    # 收益端（期望值）
    expected_ltv = row['MonthlyCharges'] * LTV_HORIZON
    expected_revenue = expected_ltv * recovery_rate

    # 淨利潤
    return expected_revenue - campaign_cost

# 4. 進行壓力測試模擬
for c in coupons:

    total_profit = simulation_df.apply(
        calculate_profit,
        axis=1,
        coupon=c
    ).sum()

    results.append({
        "Coupon": c,
        "Total_Profit": total_profit
    })

res_df = pd.DataFrame(results)
print(res_df)

# 4. 繪製「甜蜜點」尋找圖
fig, ax = plt.subplots(figsize=(10, 6))

# ROI 曲線
ax.plot(
    res_df['Coupon'],
    res_df['Total_Profit'],
    marker='o',
    color='green',
    label='Total Profit'
)

# 標記最佳點
best_idx = res_df['Total_Profit'].idxmax()
best_coupon = res_df.loc[best_idx, 'Coupon']
best_profit = res_df.loc[best_idx, 'Total_Profit']

ax.scatter(best_coupon, best_profit, color='red', s=100, zorder=5)

# 標註文字
ax.text(
    best_coupon,
    best_profit,
    f'  Best: ${best_coupon}',
    verticalalignment='bottom'
)

ax.set_xlabel('Coupon Value ($)')
ax.set_ylabel('Total Net Profit ($)')
ax.set_title('11-4-2 敏感度分析：ROI Sweet Spot')
ax.grid(True, alpha=0.3)
plt.savefig('11-4-2.png', dpi=300, bbox_inches='tight')
plt.show()

# 找出利潤最大化的面額
best_coupon = res_df.loc[res_df['Total_Profit'].idxmax(), 'Coupon']
print(f"根據模擬，最佳折扣面額為: ${best_coupon}，這將帶來最大化淨利潤。")

#%%
