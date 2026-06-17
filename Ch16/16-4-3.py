# -*- coding: utf-8 -*-

"""
16-4-3商務落地應用—從潛客評分到資源配置決策
"""

import pandas as pd
import joblib

#%%

# 延續上一小節產生的模型
# 為方便示範，重新讀入特徵表，採用舊資料

# 1. 載入模型
model = joblib.load('lead_scoring_model.pkl')

# 2. 載入並縫合最新的資料 (這一步是為了還原 df_model)
# 這裡建議直接讀取先前存好的特徵表
df_attr = pd.read_pickle('leads_with_scoring.pkl')           # 包含 Explicit_Score
df_behavior = pd.read_pickle('behavior_scores_decayed.pkl') # 包含數位熱度

# 縫合資料
df_model = pd.merge(df_attr, df_behavior, on='Lead_ID', how='left')

# 3. 處理空值與 Categorical 報錯 (延續先前的方式)
num_cols = ['Digital_Implicit_Score', 'Interaction_Count', 'Offline_Score', 'Total_Implicit_Score']
df_model[num_cols] = df_model[num_cols].fillna(0)

# 4. 定義模型需要的特徵欄位 (必須與訓練時完全一致)
features = ['Explicit_Score', 'Digital_Implicit_Score', 'Interaction_Count', 'Offline_Score']
X = df_model[features]

#%%

# --- 以下接續自動化派單邏輯 ---

# 1. 預測機率
df_model['Propensity_Score'] = model.predict_proba(X)[:, 1]

# 2. 計算百分位排名
df_model['Rank_Percentile'] = (
    df_model['Propensity_Score']
    .rank(pct=True)
)

# 3. 定義商務分級邏輯 (延用你的代碼)
def assign_tier(percentile):
    if percentile >= 0.90:
        return 'Hot'
    elif percentile >= 0.60:
        return 'Warm'
    else:
        return 'Cold'

df_model['Lead_Tier'] = df_model['Rank_Percentile'].apply(assign_tier)

# 4. 模擬自動化派單 (注意：這裡用到 Explicit_Score)
def dispatch_order(row):
    if row['Lead_Tier'] == 'Hot' and row['Explicit_Score'] > 70:
        return 'Dispatch to VIP Sales (Senior)'
    elif row['Lead_Tier'] == 'Hot':
        return 'Dispatch to Standard Sales'
    elif row['Lead_Tier'] == 'Warm':
        return 'Trigger Marketing Automation (MA)'
    else:
        return 'Put into Database (Nurturing)'

df_model['Action_Plan'] = df_model.apply(dispatch_order, axis=1)

# 5. 輸出結果
print("--- 16-4-3 商務派單自動化結果 ---")
columns_to_show = ['Lead_ID', 'Explicit_Score', 'Propensity_Score', 'Lead_Tier', 'Action_Plan']
print(df_model.sort_values(by='Propensity_Score', ascending=False)[columns_to_show].head(10))

# 6. (選做) 儲存最終派單建議表
df_model.to_excel('dispatch_list_20260510.xlsx', index=False)