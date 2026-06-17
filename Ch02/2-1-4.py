
# -*- coding: utf-8 -*-

"""
2-1-4類別資料清理與轉型
"""


import pandas as pd

# 1. 載入資料
df = pd.read_csv('E-commerce_Dirty_Dataset.csv')

# ---------------------------------------------------------------------
#  偵測階段：使用 .value_counts() 找出隱藏的內容
# ---------------------------------------------------------------------
print("未清理前的 user_type 類別分布：")
raw_counts = df['user_type'].value_counts()
print(raw_counts)
print(f"本該只有 3 類的標籤，現在被裂解成了 {len(raw_counts)} 類！")


# ---------------------------------------------------------------------
# 清理階段：使用字串函數進行「強效標準化」--視上一階段結果而定
# ---------------------------------------------------------------------
print("\n" + "-" * 70)
print("第二步：清洗--使用 .str.upper() 與 .replace() 進行結構重組")
print("-" * 70)

# 可能方式一：先將所有英文字母全部強制轉為大寫（消滅 VIP vs vip 的大小寫分歧）
df['user_type_cleaned'] = df['user_type'].str.upper()

# 可能方式二：運用映射字典，將小寫轉大寫後殘留的 'LOW' 修正回教科書標準的 'Low'，其餘保持 'Regular'
# 我們順便把 VIP、Regular、Low 的字首大寫規格統一
classification_map = {
    'VIP': 'VIP',
    'REGULAR': 'Regular',
    'LOW': 'Low'
}
df['user_type_cleaned'] = df['user_type_cleaned'].map(classification_map).astype('category')
print("清理後的 user_type 類別分布：")
raw_counts = df['user_type_cleaned'].value_counts()
print(raw_counts)

# ---------------------------------------------------------------------
# 驗證階段：重新聚合
# ---------------------------------------------------------------------
print("\n第三步：最終驗證 清理與標準化後的 user_type 類別分布：")
clean_counts = df['user_type_cleaned'].value_counts()
print(clean_counts)
print(f"類別數量目前是 {len(clean_counts)} 大核心群體，無痛接軌後續商業分析！")
print("=" * 70)

df.info()
