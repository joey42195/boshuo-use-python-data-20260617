
"""
3-1-1為什麼資料視覺化如此重要？
"""

import pandas as pd

# 1. 基礎長表
long_breakfast = pd.DataFrame({
    '顧客ID': ['C001', 'C001', 'C002', 'C002'],
    '產品': ['茶', '蛋餅', '茶', '漢堡'],
    '金額': [120, 150, 100, 200]
})

# ==========================================
# 步驟 2：長表轉寬表 (Reshaping: Long to Wide)
# ==========================================
# 目的：將原本「一列代表一次交易」的交易明細（長表），
#       轉換成「一列代表一個客戶」的客戶消費輪廓表（寬表），方便後續建模或計算消費總額。
wide_breakfast = long_breakfast.pivot(
    index='顧客ID',    # 以「顧客」為單位，每位顧客橫跨成唯一的一列
    columns='產品',   # 將所有不同的「產品品項」攤開，轉化為新的多個欄位（如：蛋餅、奶茶...）
    values='金額'     # 欄位與列的交叉點，填入該顧客購買該產品的「金額」
)

# ==========================================
# 步驟 3：寬表商務優化與補 0 (Data Cleaning)
# ==========================================
# 目的：消除轉換寬表後產生的空值，並優化資料型態以符合商務報表直覺。
wide_breakfast_clean = (
    wide_breakfast
    .fillna(0)        # 商務邏輯補值：如果顧客沒買過某產品，Pandas 會產生 NaN。在商業上，沒買代表消費金額為「0 元」
    .astype(int)      # 型態轉換：金額在早餐店情境下通常是整數，將浮點數（float）轉為整數（int）更易閱讀
    .reset_index()    # 釋放索引：將原本變成 Index 的 '顧客ID' 重新變回正常的 DataFrame 欄位，方便後續合併或存檔
)

print("=" * 65)
print("商務寬表 (Wide-form)")
print("=" * 65)
print(wide_breakfast_clean.to_string(index=False))

# 4. 核心技術：利用 melt() 將寬表重新「融化」還原為【長格式 (Long-form)】
# id_vars: 固定不動的識別基準（主體）
# value_vars: 要被拆解、由橫轉直的特徵欄位（如果不寫，預設會融化除 id_vars 以外的所有欄位）
restored_long = pd.melt(
    wide_breakfast_clean,
    id_vars=['顧客ID'],   # ：固定不動的識別欄位
    value_vars=['茶', '蛋餅', '漢堡'],   #要被轉換的欄位
    var_name='產品',   # 數值欄位名稱
    value_name='金額'
)

# 商務過濾：原本補 0 的格子代表現實中「沒購買」，還原成长表時應將 金額 > 0 的紀錄篩選出來
restored_long_clean = restored_long[restored_long['金額'] > 0].sort_values(by=['顧客ID']).reset_index(drop=True)

print("\n" + "=" * 65)
print("利用 melt() 還原的【標準長格式 (Long-form)】")
print("=" * 65)
print(restored_long_clean.to_string(index=False))
print("=" * 65)
