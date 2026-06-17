
# -*- coding: utf-8 -*-

"""
2-4-1類別資料編碼
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder

# 1. 載入資料
df = pd.read_csv('E-commerce_Dirty_Dataset.csv')


# 快速前置清洗（確保類別乾淨，延用第 2 章成果）
df['user_type'] = df['user_type'].str.upper().replace({'VIP':'VIP', 'REGULAR':'Regular', 'LOW':'Low'})

# ---------------------------------------------------------------------
# 實戰一：Label Encoding ➔ 應用於具備順序階級的 user_type
# ---------------------------------------------------------------------
print("\n實戰一 對具備業務階級階層的 'user_type' 使用 Label Encoding")

# 方式 A：Pandas 內建 cat.codes（適合 EDA 與快速觀察）
df['user_type_cat'] = df['user_type'].astype('category')
print(df['user_type_cat'])
df['user_type_pandas_code'] = df['user_type_cat'].cat.codes
print(df['user_type_pandas_code'])

# 方式 B：Scikit-learn LabelEncoder（正式建模與 Pipeline 接軌標準）
# 建立編碼器
from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()

# 進行 Label Encoding
df['user_type_code'] = (
    encoder.fit_transform(df['user_type'])
)
print("   - 編碼對照 撈出前 5 筆看清文字與數字代碼的映射關係：")
print(df[['user_type', 'user_type_code']].head(5))
print(f"   ➔ 映射字典對照: {dict(zip(encoder.classes_, encoder.transform(encoder.classes_)))}")


# ---------------------------------------------------------------------
# 實戰二：One-Hot Encoding ➔ 應用於無順序高低的 gender (性別)
# ---------------------------------------------------------------------
print("\n" + "-" * 80)
print("實戰二 對不具備順序關係的 'gender' 使用 One-Hot Encoding")
print("-" * 80)

# 使用 pd.get_dummies()，為了商務美觀，我們加上 prefix 識別字首
# dtype=int 參數能讓輸出的 True/False 自動轉為標準的 1 與 0
df_gender_encoded = pd.get_dummies(df['gender'], prefix='gender', dtype=int)

print("   - 獨熱拆解 看看原本的 gender 欄位是如何被裂變為獨立特徵矩陣的：")
print(pd.concat([df['gender'], df_gender_encoded], axis=1).head(5))
print("\n   核心觀察 模型不再理解大小，而是理解『是否為女性 (gender_F)』與『是否為男性 (gender_M)』")
print("=" * 80)


