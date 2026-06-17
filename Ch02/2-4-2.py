
# -*- coding: utf-8 -*-

import pandas as pd

"""
2-4-2時間欄位拆解
"""

# 1. 載入資料
df = pd.read_csv('E-commerce_Dirty_Dataset.csv')


# ---------------------------------------------------------------------
# 前置防線：先強制轉型（呼應 2-1-2，否則拆解特徵會報錯！）
# ---------------------------------------------------------------------
# 遇到 "2024/13/40" 或 "not available" 一律化為標準 NaT (Not a Time)
df['signup_date_clean'] = pd.to_datetime(df['signup_date'], errors='coerce')
df['last_active_date_clean'] = pd.to_datetime(df['last_active_date'], errors='coerce')


# ---------------------------------------------------------------------
# 使用 .dt 進行時間維度大拆解
# ---------------------------------------------------------------------
print("\n特徵拆解 對乾淨的註冊日期使用 .dt 屬性抽取...")

# 1. 抽取年、月、日
df['signup_year'] = df['signup_date_clean'].dt.year
df['signup_month'] = df['signup_date_clean'].dt.month
df['signup_day'] = df['signup_date_clean'].dt.day

# 2. 抽取星期幾 (Pandas 預設：0 = 星期一, 6 = 星期日)
df['signup_weekday'] = df['signup_date_clean'].dt.weekday

# 3. 商業邏輯延伸：運用布林判斷，生成「是否為週末 (is_weekend)」標籤
# 只要 weekday >= 5 (代表 5 是週六、6 是週日)，即為 True，再乘以 1 轉為 0/1 訊號
df['is_weekend'] = (df['signup_weekday'] >= 5).astype(int)


# ---------------------------------------------------------------------
# 成果展現：看時間是如何變成「行為特徵」的
# ---------------------------------------------------------------------
print("\n" + "-" * 80)
print("拆解成果對照 撈出前 5 筆：")
print("-" * 80)

output_cols = ['signup_date', 'signup_year', 'signup_month', 'signup_weekday', 'is_weekend']
print(df[output_cols].head(5))

print("\n" + "-" * 80)
print("利用剛剛拆解出的特徵，快速透視週末與週間的註冊分布：")
print("-" * 80)
# 統計 is_weekend 欄位中各類別的出現比例（百分比）
weekend_distribution = (
    df['is_weekend']
    
    # 計算各類別出現次數
    # normalize=True 代表「不要回傳原始筆數」
    # 而是回傳「比例」(百分比前的 0~1 小數)
    .value_counts(normalize=True)
    
    # 轉換成百分比
    * 100
)
print(f"   - 平日 (週間 0-4) 註冊佔比 : {weekend_distribution[0]:.2f}%")
print(f"   - 假日 (週末 5-6) 註冊佔比 : {weekend_distribution[1]:.2f}%")



