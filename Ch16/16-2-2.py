# -*- coding: utf-8 -*-

"""
16-2-2屬性維度評分實作—潛客資格的門檻建構
"""

import pandas as pd
import numpy as np

# --- 1. 載入資料集 ---
df_leads = pd.read_csv('leads.csv')
# df_digital = pd.read_csv('digital_logs.csv', parse_dates=['Timestamp'])
# df_offline = pd.read_csv('offline_interactions.csv', parse_dates=['Interaction_Date'])

# --- 2. 定義「資格門檻」與「屬性權重邏輯」 ---
# 這些變數可以根據商務需求隨時調整
INCOME_THRESHOLD = 300  # 年收門檻（萬元）
SOURCE_WEIGHTS = {
    'Referral': 30,       # 推薦來源加分最高
    'Offline Event': 20,  # 參加過實體活動
    'Google Search': 10,  # 主動搜索
    'FB Ads': 5           # 廣告投放
}
# # 目前沒用到，沒工作欄位。僅示意
# JOB_WEIGHTS = {'C-Level': 30, 'Owner': 30, 'Manager': 15, 'Junior': 0}

def calculate_explicit_score(row):
    """
    計算屬性維度（靜態標籤）的得分
    """
    # 【一票否決邏輯】：財務能力未達標，分數直接歸零
    # 這裡假設你的 CSV 欄位名稱是 Annual_Income_Est
    if row['Annual_Income_Est'] < INCOME_THRESHOLD:
        return 0
    
    score = 0
    
    # A. 來源特徵加分 (Source)
    score += SOURCE_WEIGHTS.get(row['Source'], 0)
    
    # B. 財務能力線性加分
    # 邏輯：每 50 萬增加 1 分，最高上限 50 分(設定上限避免離群值影響過大)
    income_bonus = min(row['Annual_Income_Est'] / 50, 50) 
    score += income_bonus
    
    # C. 年齡區間加分 (假設 40-55 歲為高單價主力客群)
    if 40 <= row['Age'] <= 55:
        score += 20

    # # D. 職業特徵加分，僅示意，目前無此資料
    # score += JOB_WEIGHTS.get(row['Job_Level'], 0)  

    # # E. 服務輻射區加分 (若不在服務區，成交難度高，權重降低)，僅示意，目前無此資料
    # if row['In_Service_Area']:
    #     score += 20
      
    return score

# --- 3. 執行評分 ---
# 將邏輯應用到讀入的 df_leads
df_leads['Explicit_Score'] = df_leads.apply(calculate_explicit_score, axis=1)

# # --- 4. 定義「潛客天花板」等級 ---
# # 分數低於 40：Low-Cap (品牌感知級)
# # 分數 40-70：Mid-Cap (重點追蹤級)
# # 分數 > 70  ：High-Cap (頂級優先級)
# df_leads['Tier_Ceiling'] = pd.cut(
#     df_leads['Explicit_Score'], 
#     bins=[-1, 40, 70, 1000], 
#     labels=['Low-Cap', 'Mid-Cap', 'High-Cap']
# )

# 三個標籤，但用百分位數來切（例如：0-50%, 50-75%, 75-100%）：
df_leads['Tier_Ceiling'] = pd.qcut(
    df_leads['Explicit_Score'], 
    q=[0, 0.5, 0.75, 1], 
    labels=['Low-Cap', 'Mid-Cap', 'High-Cap']
)


# --- 5. 輸出分析結果 ---
print("-" * 30)
print(f"資料讀取筆數：{len(df_leads)}")
print("天花板等級分布：")
print(df_leads['Tier_Ceiling'].value_counts())
print("-" * 30)

# 顯示前 5 名具備高潛力的客戶 (High-Cap)
print("高潛力客戶 (High-Cap) 樣本：")
print(df_leads.head())
print(df_leads[df_leads['Tier_Ceiling'] == 'High-Cap'].head())

# --- 6. 儲存結果 ---
# 存成一個新的 Pickle 檔，完整保留資料型別與分級標籤
df_leads.to_pickle('leads_with_explicit_scores.pkl')


#%%

# --- 6. 儲存中間產物 (為 16-4 回歸模型做準備) ---

# 選擇回歸模型需要的關鍵欄位
# Lead_ID: 串聯用
# Converted: 目標變數 (Y)
# Explicit_Score: 屬性特徵 (X1)
# Tier_Ceiling: 類別特徵 (X2, 可轉為 Dummy variables)

df_to_save = df_leads[['Lead_ID', 'Explicit_Score', 'Tier_Ceiling', 'Converted']]

# 儲存為 pickle
df_to_save.to_pickle('leads_with_scoring.pkl')
df_to_save.to_csv('leads_with_scoring.csv', index=False)

print(f"\n[系統訊息] 已成功產出回歸預備檔案：leads_with_scoring.csv")
print(f"包含欄位：{df_to_save.columns.tolist()}")





