
# -*- coding: utf-8 -*-

"""
2-2-3缺失值處理策略
"""

import pandas as pd
import numpy as np

# 1. 載入資料
df = pd.read_csv('E-commerce_Dirty_Dataset.csv')
df.info()

# 在動手之前，先將原始資料備份三份，分別實驗三種策略
df_strategy1 = df.copy()
df_strategy2 = df.copy()
df_strategy3 = df.copy()

# 先行清除 user_type 的大小寫干擾（沿用 2-1-3 成果，確保分組正確）
for d in [df_strategy1, df_strategy2, df_strategy3]:
    d['user_type'] = d['user_type'].str.upper().replace({'VIP':'VIP', 'REGULAR':'Regular', 'LOW':'Low'})


# ---------------------------------------------------------------------
# 策略一：刪除法 (Deletion) ➔ 簡單粗暴的雙面刃
# ---------------------------------------------------------------------
print("\n策略一 使用 dropna() 直接刪除缺失值：")
print(f"   - 處理前資料總筆數: {len(df_strategy1)} 筆")

# 僅針對特定核心欄位（如消費金額）若有缺失就剔除
df_strategy1_cleaned = df_strategy1.dropna(subset=['spending'])
print(f"   - 僅刪除 spending 缺失後筆數: {len(df_strategy1_cleaned)} 筆")

# 全欄位一刀切刪除
df_strategy1_extreme = df_strategy1.dropna()
print(f"   - 全欄位一刀切 dropna() 後殘存筆數: {len(df_strategy1_extreme)} 筆")


# ---------------------------------------------------------------------
# 策略二：統計補值 (Statistical Imputation) ➔ 大眾盲從的平均數迷思
# ---------------------------------------------------------------------
print("\n" + "-" * 80)
print("策略二 使用 fillna() 總平均數補值：")
print("-" * 80)

# 先強制轉換為數值型態（沿用 2-1-2 的型別清理成果）
df_strategy2['income'] = pd.to_numeric(
    df_strategy2['income'],
    errors='coerce'
)
print(f"   - income 的缺失情形 : {df['income'].isnull().sum():.0f} 筆")

# 補值前：先觀察目前「非缺失值」的平均收入
original_income_mean = df_strategy2['income'].mean()
print(f"   - 補值前平均收入: {original_income_mean:.2f} 元")


# 使用全站平均值填補所有 income 缺失值
df_strategy2['income_filled_global'] = (
    df_strategy2['income']
    .fillna(original_income_mean)
)

# # 2. 自行測試---使用中位數填補所有 income 缺失值
# # 3. 計算原本「非缺失值」的中位數
# original_income_median = df_strategy2['income'].median()
# df_strategy2['income_filled_global'] = (
#     df_strategy2['income']
#     .fillna(original_income_median)
# )


# 補值後再次計算平均值
filled_income_mean = (
    df_strategy2['income_filled_global']
    .mean()
)
print(f"   - 補值後平均收入: {filled_income_mean:.2f} 元")

# ---------------------------------------------------------------------
# 策略三：商業邏輯補值 (Business Logic Imputation) ➔ 精準修補
# ---------------------------------------------------------------------
print("\n" + "-" * 80)
print("策略三 使用 groupby() 依據「用戶級別」進行條件特徵補值：")
print("-" * 80)

df_strategy3['income'] = pd.to_numeric(df_strategy3['income'], errors='coerce')

# 商業邏輯：VIP、Regular、Low 的收入天差地遠，補值必須依照「各自群體的平均數」來補！
# 我們利用 groupby().transform() 功能，幫每筆缺失值自動對號入座
# 使用「商業邏輯分組補值」
# 不同 user_type（VIP、Regular、Low）使用各自群組的平均收入補值

df_strategy3['income_filled_logic'] = (
    
    # 對 income 欄位中的缺失值（NaN）進行填補
    df_strategy3['income'].fillna(
        
        # 依照 user_type 進行分組
        df_strategy3
        .groupby('user_type')['income']
        
        # 計算每個群組的平均收入
        # transform('mean') 會將「群組平均值」
        # 映射回原始資料的每一列
        .transform('mean')
    )
)


# =====================================================================
# 商務回測：兩種補值策略如何改變了數據的真實面貌？
# =====================================================================
print("\n" + "=" * 80)
print(" [策略效果對照] 看看 Low (低活躍用戶) 被補值後的結果：")
print("=" * 80)

# 觀察 Low 用戶在經過「策略二」與「策略三」後的平均收入變化
low_compare = pd.DataFrame({
    '策略二：直托使用平均值': [df_strategy2[df_strategy2['user_type'] == 'Low']['income_filled_global'].mean()],
    '策略三：商業邏輯補值': [df_strategy3[df_strategy3['user_type'] == 'Low']['income_filled_logic'].mean()]
}, index=['Low 用戶補值後的平均收入'])

print(low_compare)
# =====================================================================
# 全體商務回測：補值策略如何改變了「所有客群」的真實面貌？
# =====================================================================
print("\n" + "=" * 80)
print("全客群策略效果對照 各組用戶被補值後的真實平均收入：")
print("=" * 80)

# 1. 計算純粹排除缺失值後的「各組真實原始平均收入」（控制組）
# 為了避免負數地雷干擾，我們先排除負數與 NaN，建立最純淨的對照基準
df_clean_baseline = df.copy()
df_clean_baseline['user_type'] = df_clean_baseline['user_type'].str.upper().replace({'VIP':'VIP', 'REGULAR':'Regular', 'LOW':'Low'})
df_clean_baseline['income'] = pd.to_numeric(df_clean_baseline['income'], errors='coerce')
df_clean_baseline = df_clean_baseline[df_clean_baseline['income'] > 0] # 排除負數地雷
baseline_income = df_clean_baseline.groupby('user_type')['income'].mean()

# 2. 計算策略二（盲補）之後，各組的平均收入
strategy2_income = df_strategy2.groupby('user_type')['income_filled_global'].mean()

# 3. 計算策略三（商業邏輯補值）之後，各組的平均收入
strategy3_income = df_strategy3.groupby('user_type')['income_filled_logic'].mean()

# 4. 完美收攏成「全客群審判矩陣」
full_compare = pd.DataFrame({
    '基準點：未補值的真實均值 (元)': baseline_income,
    '策略二：直接使用全站平均 (元)': strategy2_income,
    '策略三：商業邏輯分組補值 (元)': strategy3_income
})

# 調整一下列印順序，讓 VIP 在最上面，符合商務大盤直覺
print(full_compare.reindex(['VIP', 'Regular', 'Low']).round(2))

