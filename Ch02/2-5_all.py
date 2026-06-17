
# -*- coding: utf-8 -*-

"""
2-5資料品質與合理性檢查
"""

import pandas as pd
import numpy as np

# 1. 載入資料
df = pd.read_csv('E-commerce_Dirty_Dataset.csv')

# =====================================================================
#  2-5-1 數值範圍檢查 (Range Check) ➔ 找出不合理的物理地雷
# =====================================================================
print("\n2-5-1 數值範圍體檢 正在揪出違反物理世界的極端異端...")

# 先強制轉換型態以利計算
df['income'] = pd.to_numeric(df['income'], errors='coerce')
df['conversion_rate_raw'] = pd.to_numeric(df['conversion_rate'], errors='coerce')

# 規則：收入不能為負數
negative_income = df[df['income'] < 0]
# 規則：轉換率理論上不能大於 1.0 (100%)
over_conversion = df[df['conversion_rate_raw'] > 1.0]

print(f"   - 抓到「負數收入」資料: {len(negative_income)} 筆")
print(f"   - 抓到「轉換率爆表(>100%)」資料: {len(over_conversion)} 筆")


# =====================================================================
# 2-5-2 業務規則驗證 (Business Rules) ➔ 戳破身分不符的偽裝者
# =====================================================================
print("\n" + "-" * 80)
print("2-5-2 業務規則 依據電商規則，驗證用戶行為是否符合「身分設定」...")
print("-" * 80)

# 清理用戶類別字串
# 先全部轉小寫，再對照換成想要的最終格式
df['user_type'] = df['user_type'].str.lower().replace({
    'vip': 'VIP',
    'regular': 'Regular',
    'low': 'Low'
})
df['spending'] = pd.to_numeric(df['spending'], errors='coerce')

# 商業規則設定：在我們平台上，Low (低活躍用戶) 的單筆消費不可能超過 100,000 元
# 如果超過了，不是系統記錯，就是他其實是漏網的 VIP 大戶！
violate_business_rule = df[(df['user_type'] == 'Low') & (df['spending'] > 100000)]

print(f"   - 抓到「身分不符」的邏輯衝突數據: {len(violate_business_rule)} 筆")
if len(violate_business_rule) > 0:
    print("     衝突樣本抽樣顯示：")
    print(violate_business_rule[['user_id', 'user_type', 'spending']].head(2))


# =====================================================================
# 2-5-3 重複值檢查 (Duplicates) ➔ 辨識重複的「本質來源」
# =====================================================================
print("\n" + "-" * 80)
print("2-5-3 重複值溯源 檢查資料中的重複紀錄，並釐清其業務本質...")
print("-" * 80)

# A. 完整資料列完全重複（通常是系統逆物流或重複上傳 Bug）
exact_duplicates = df.duplicated()
print(f"   - 全欄位完全是重複的資料: {exact_duplicates.sum()} 筆")
print(exact_duplicates)

# B. 關鍵字欄位重複，但其他行為資料不同（通常是同用戶在不同 Log 中的自然行為）
user_id_duplicates = df.duplicated(subset=['user_id'], keep=False)
print(f"   - 同一 user_id 在大盤中多次現身(行為 Log 自然現象): {user_id_duplicates.sum()} 筆")
print(user_id_duplicates)

# =====================================================================
# 2-5-4 資料一致性問題 (Consistency) ➔ 降伏單位與格式的混亂
# =====================================================================
print("\n" + "-" * 80)
print("2-4-4 一致性對齊 解除單位與格式混亂（元 vs 千元 / 小數 vs 百分比）...")
print("-" * 80)

# 模擬真實場景中：部分資料是用「台幣(元)」，部分海外主管輸入的是「千元」或「美金(以百為單位)」
# 我們檢查若收入欄位異常小於 1000 且大於 0，高機率是誤用了「千元」為單位
# 使用 np.where() 進行條件式資料修正（向量化操作）
# 語法結構：
# np.where(條件, 條件成立時的值, 條件不成立時的值)

df['income_aligned'] = np.where(

    # 條件判斷：
    # 若 income 小於 1000，
    # 在商業情境中高度懷疑是「單位輸入錯誤」
    # 例如原本應該輸入「50000 元」，
    # 卻被寫成「50（代表50千元）」。
    df['income'] < 1000,

    # 條件成立時：
    # 將數值乘上 1000，
    # 統一回「元」的單位
    df['income'] * 1000,

    # 條件不成立時：
    # 保持原始 income 數值不變
    df['income']
)

print(f"   - 調整前收入中位數: {df['income'].median():.2f} 元")
print(f"   - 修正「千元制單位」後收入中位數: {df['income_aligned'].median():.2f} 元")
print("   成功 一致性對齊完畢，我們終於是在比較『同一種東西』了！")
print("=" * 80)