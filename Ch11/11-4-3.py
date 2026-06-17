# -*- coding: utf-8 -*-

"""
11-4-3流失挽回的決策分層—避免資源錯配與利潤稀釋
"""

import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score, accuracy_score
import numpy as np
import joblib
import matplotlib.pyplot as plt

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_pickle('Telco-Customer-Churn_11-2-3.pkl')

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
# 4. 重新定義 X 與 y (只取數值欄位)
X = df[features]
y = df['Churn']

# 現在執行 train_test_split 與後續的 model.fit 就不會報錯了！
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 1. 載入 存好的優化模型
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
MARKETING_OPEX = 5         # 推播簡訊與行政成本
RECOVERY_RATE = 0.25       # 挽回成功率 (修正：並非 100% 的人拿了券都會留下)
LTV_HORIZON = 6            # 我們看接下來 6 個月的營收貢獻

# 3. 計算各群組的「發券損益」
# 參數：假設最優折扣為 20 元 (從 10-5-2 得知)
COUPON = 25
LTV_6M = 6

# 3. 定義「高風險群」：只有流失機率 > 0.6 的人才發券 (精準打擊)
simulation_df['Target_Action'] = simulation_df['Churn_Prob'] > 0.6

# 1. 計算「全量發放 (Blind All)」的預期利潤
# 假設所有人不論風險高低都發券
def calc_blind_profit(row):
    coupon_cost = (COUPON * 3) + 5
    # 對於忠誠者，發券是純損失；對於猶豫者與心死者，才有挽回收益
    if row['Churn_Prob'] < 0.4:
        return -coupon_cost
    else:
        return (row['MonthlyCharges'] * LTV_6M * RECOVERY_RATE) - coupon_cost

simulation_df['Profit_Blind_All'] = simulation_df.apply(calc_blind_profit, axis=1)

# 2. 計算「精準打擊 (Targeted)」的預期利潤
# 只針對建議的區間 發券，其餘不發 (利潤貢獻為 0)
def calc_targeted_profit(row):
    if row['Churn_Prob'] < 0.4 or row['Churn_Prob'] > 0.8:
        return 0 # 忠誠者，不會回頭的不發券，不賺不賠
    else:
        # 僅針對高風險群體計算 (承接先前的計算邏輯)
        coupon_cost = (COUPON * 3) + 5
        return (row['MonthlyCharges'] * LTV_6M * RECOVERY_RATE) - coupon_cost

simulation_df['Profit_Targeted'] = simulation_df.apply(calc_targeted_profit, axis=1)

# 3. 彙總對比報表
strategy_comparison = pd.DataFrame({
    '策略名稱': ['盲目全量發放 (Blind All)', 'AI 精準打擊 (Targeted)'],
    '受贈人數': [len(simulation_df), simulation_df[simulation_df['Churn_Prob'] >= 0.3].sum()['Target_Action']],
    '預估總利潤': [simulation_df['Profit_Blind_All'].sum(), simulation_df['Profit_Targeted'].sum()],
    '平均每人獲利力': [simulation_df['Profit_Blind_All'].mean(), simulation_df['Profit_Targeted'].mean()]
})

print("--- 10-5-3 策略對比戰報：AI 避險的價值 ---")
print(strategy_comparison)

# 4. 視覺化對比
strategy_comparison.set_index('策略名稱')['預估總利潤'].plot(kind='bar', color=['salmon', 'skyblue'], figsize=(8, 6))
plt.title('Profit Comparison: Blind All vs. Targeted Strategy')
plt.ylabel('Total Estimated Profit ($)')
plt.axhline(0, color='black', linewidth=0.8)
plt.xticks(rotation=0)
plt.show()
