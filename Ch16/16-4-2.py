# -*- coding: utf-8 -*-

"""
16-4-2建立潛客評分模型—用機率量化成交可能性
"""


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score

# 1. 載入兩大特徵表
df_attr = pd.read_pickle('leads_with_scoring.pkl')       # 來自 16-2
df_behavior = pd.read_pickle('behavior_scores_decayed.pkl') # 原來自 16-3，16-4-1加上時間衰減

#%%

# 我們要把 16-2 的「身分實力」與 16-3 的「行為熱度」縫合在一起。

# 2. 進行縫合
# 使用 Left Join，確保所有 Lead 都在，沒行為的補 0
# 不能直接補 0，(避免 Categorical 報錯)
df_model = pd.merge(df_attr, df_behavior, on='Lead_ID', how='left')


# A. 針對數值型欄位補 0 (這些才是迴歸要用的 X)
num_cols = ['Digital_Implicit_Score', 'Interaction_Count', 'Offline_Score', 'Total_Implicit_Score']
df_model[num_cols] = df_model[num_cols].fillna(0)

# B. 針對類別型欄位補 "Unknown" 或 "Low-Cap" (如果要保留類別的話)
# 如果模型暫時用不到 Tier_Ceiling，也可以先不管它
if 'Tier_Ceiling' in df_model.columns:
    # 先增加一個分類選項叫 "None"
    df_model['Tier_Ceiling'] = df_model['Tier_Ceiling'].cat.add_categories(["None"])
    df_model['Tier_Ceiling'] = df_model['Tier_Ceiling'].fillna("None")

print("--- 資料縫合完成且補值成功 ---")
print(df_model.info())

#%%



# 3. 定義 X (自變數) 與 y (目標標籤)
# 我們選取：屬性分、數位衰減熱度、互動頻次、線下分數
features = ['Explicit_Score', 'Digital_Implicit_Score', 'Interaction_Count', 'Offline_Score']
X = df_model[features]
y = df_model['Converted']

print("--- 特徵矩陣 (X) 預覽 ---")
print(X.head())

#%%

# 建立邏輯迴歸模型
# 邏輯迴歸最迷人的地方在於它不僅給出「是/否」，還會給出「機率（0 ~ 1 之間）」。

# 1. 切分訓練集與測試集 (80% 訓練, 20% 驗證)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. 初始化並訓練模型
model = LogisticRegression()
model.fit(X_train, y_train)

# 3. 預測機率
y_prob = model.predict_proba(X_test)[:, 1] # 取得「成交」的機率
y_pred = model.predict(X_test)

# 4. 模型效能評估
print("\n--- 模型效能報告 ---")
print(classification_report(y_test, y_pred))
print(f"AUC 曲線下面積: {roc_auc_score(y_test, y_prob):.4f}")

#%%
# 調整判定門檻為 0.3
y_pred_adj = (y_prob >= 0.3).astype(int)

print("--- 調整門檻 (Threshold=0.3) 後的報告 ---")
print(classification_report(y_test, y_pred_adj))



#%%


# 讀「係數」：誰才是最強預測因子？
# 最重要圖表。
# 我們可以解讀：到底是「年收」重要，還是「預約試駕」重要？

# 提取模型係數
coef_df = pd.DataFrame({
    'Feature': features,
    'Coefficient': model.coef_[0]
}).sort_values(by='Coefficient', ascending=False)

print("\n--- 行為與屬性之影響力分析 ---")
print(coef_df)

#%%

# ===== 儲存模型 =====
import joblib

joblib.dump(model, 'lead_scoring_model.pkl')

print("\n模型已成功儲存")



