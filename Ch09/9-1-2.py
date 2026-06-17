# -*- coding: utf-8 -*-

"""
9-1-2 Funnel分析前的資料可信度檢查
"""

import pandas as pd

# 載入資料
df = pd.read_csv('funnel.csv')
df.columns

"""
一、 確立漏斗的核心事件
"""
# 查看事件類型
# 檢查資料集中的事件類型與基礎計數
print("【事件類型分布檢視】")
print(df['event'].value_counts())

#%%
"""
二、 辨識漏斗的關鍵分析維度
"""
features = [
    'channel',   # 流量來源（評估渠道質量與獲客成本）
    'device',    # 裝置體驗（評估 RWD 響應式網頁或 App 的技術相容性）
    'region',    # 地理區域（評估地域性物流、文化偏好或市場成熟度）
    'category',  # 商品品類（評估商品結構、定價策略與庫存健全度）
    'campaign'   # 行銷活動（評估特定促銷案的拉新與轉化效果）
]

for col in features:
    print(df[col].value_counts())  # 檢視前類別分布

#%%
"""
三、 驗證行為序列的合規性（Event Flow Validation）
"""

# 將資料依照使用者 ID 與時間戳記進行正向排序，還原真實行為軌跡
df = df.sort_values(['user_id', 'timestamp']).reset_index(drop=True)
 
# 抽樣檢視部分使用者的事件流序列
print("【使用者行為序列抽樣（前 20 筆）】")
print(df[['user_id', 'timestamp', 'event']].head(20))


# 查看部分事件流
# 1. 找出所有曾發生過購買行為（purchase）的獨立使用者
purchase_users = df[df['event'] == 'purchase']['user_id'].unique()
 
# 2. 找出所有曾將商品加入購物車（add_to_cart）的獨立使用者
cart_users = df[df['event'] == 'add_to_cart']['user_id'].unique()
 
# 3. 利用集合相減，找出「有購買、卻沒有加入購物車紀錄」的異常使用者
invalid_users = set(purchase_users) - set(cart_users)

# 4. 輸出檢驗結果
print(f"總購買人數: {len(purchase_users)} 人")
print(f"異常漏斗（無購物車紀錄卻完成購買）人數: {len(invalid_users)} 人")
if len(invalid_users) > 0:
    print(f"警示：異常比例達 {(len(invalid_users)/len(purchase_users))*100:.2f}%，建議先與技術團隊校對埋點邏輯。")
else:
    print("檢查通過：事件流邏輯完全合規，可正式進入漏斗診斷。")
