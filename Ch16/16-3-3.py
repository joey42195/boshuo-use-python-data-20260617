# -*- coding: utf-8 -*-

"""
16-3-3行為評分實作與特徵持久化
"""

import pandas as pd
import numpy as np
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_columns', 20)

# 載入資料集
df_leads = pd.read_csv('leads.csv')
df_digital = pd.read_csv('digital_logs.csv', parse_dates=['Timestamp'])
df_offline = pd.read_csv('offline_interactions.csv', parse_dates=['Interaction_Date'])

# 1. 行為維度指標設計

# --- [策略 1：行為權重化 (Action Weighting)] ---
# 定義商務權重字典，或「行為價值表」 (由分析師與業務主管共同定義)
# 反映不同行為背後的心理門檻 
BEHAVIOR_WEIGHTS = { 
    'view_homepage': 2, # 品牌認知 
    'view_warranty': 10, # 產品評估 (關心售後) 
    'view_spec_page': 15, # 產品評估 (深度對比) 
    'download_catalog': 20, # 意圖增溫 
    'use_finance_calc': 40, # 決策準備 (計算購買力) 
    'book_test_drive': 60 # 成交前置 (實體轉化) 
}


# 將權重映射回原始日誌 (確保 Behavior_Score 欄位正確反映定義)
df_digital['Behavior_Score'] = df_digital['Action'].map(BEHAVIOR_WEIGHTS).fillna(0)

# 顯示權重化後的日誌範例
print("數位行為權重化結果：")
print(df_digital[['Lead_ID', 'Action', 'Behavior_Score']].head())


#%%


# --- [累計熱量 與 互動頻次] ---
# 使用 groupby 將同一個 Lead_ID 的行為加總
df_digital_aggregated = df_digital.groupby('Lead_ID').agg(
    Digital_Implicit_Score=('Behavior_Score', 'sum'), # 累計熱量 (Sum)
    Interaction_Count=('Action', 'count')             # 互動頻次 (Count)
).reset_index()

# --- [線上與線下的縫合 (O2O Stitching)] ---
# 1. 處理線下數據 (df_offline 可能有多筆，也需先聚合)
df_offline_aggregated = df_offline.groupby('Lead_ID').agg(
    Offline_Score=('Duration_Min', 'sum')
).reset_index()



# 2. 進行跨渠道縫合 (使用 Outer Join 確保只在線上或線下出現的潛客都被保留)
df_behavior_total = pd.merge(
    df_digital_aggregated, 
    df_offline_aggregated, 
    on='Lead_ID', 
    how='outer'
).fillna(0) # 沒出現代表沒行為，補 0

# 3. 計算總熱力值
df_behavior_total['Total_Implicit_Score'] = (
    df_behavior_total['Digital_Implicit_Score'] + 
    df_behavior_total['Offline_Score']
)

# --- 輸出結果展示 ---
print("--- 潛客行為熱度分析 (Top 5) ---")
print(df_behavior_total[['Lead_ID', 'Digital_Implicit_Score', 'Offline_Score', 'Total_Implicit_Score']].sort_values(by='Total_Implicit_Score', ascending=False).head())

#%%

# --- [15-3 結尾：特徵儲存] ---

# 整理 15-4 需要的行為特徵欄位
behavior_features = df_behavior_total[[
    'Lead_ID', 
    'Digital_Implicit_Score', 
    'Interaction_Count', 
    'Offline_Score', 
    'Total_Implicit_Score'
]]

# 儲存為 behavior_scores.pkl (保留浮點數精度與結構)
behavior_features.to_pickle('behavior_scores.pkl')

print("\n[系統訊息] 16-3 行為維度計算完成。")
print(f"已識別 {len(behavior_features)} 位具備行為軌跡的潛客，特徵已存至 behavior_scores.pkl")



