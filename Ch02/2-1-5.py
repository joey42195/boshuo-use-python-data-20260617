# -*- coding: utf-8 -*-


"""
2-1-5時間資料與格式問題
"""

import pandas as pd


# 1. 載入髒數據大盤
df = pd.read_csv('E-commerce_Dirty_Dataset.csv')
df.info()   # last_active_date 目前不是日期格式

# ---------------------------------------------------------------------
# 為什麼盲目使用 .astype() 會直接炸裂？
# ---------------------------------------------------------------------
print("\n 如果我們對含有髒字串的時間欄位盲目使用 .astype()...")
# 觀察錯誤後，請註解此行
df['last_active_date'].astype('datetime64[ns]')  # 這行會報錯

try:     # 轉型時，最好使用例外偵測
    # 嘗試強行將含有 "not available" 的欄位轉為 datetime
    df['last_active_date'].astype('datetime64[ns]')
except Exception as e:
    print(f"系統報錯！錯誤訊息為: {e}")


# ---------------------------------------------------------------------
# 時間欄位的安全轉換 (pd.to_datetime)
# ---------------------------------------------------------------------
print("\n" + "-" * 70)
print(" 使用 pd.to_datetime + errors='coerce' 找出偽裝時間")
print("-" * 70)

print("偵測 last_active_date 中，隱藏了多少無法辨識的『偽裝時間』字串？")
print(df['last_active_date'].isna().sum())
dirty_date_samples = df[df.isnull()]['last_active_date'].unique()

# 1. 把轉換後的結果存到「新欄位」，保留舊欄位
df['clean_date'] = pd.to_datetime(df['last_active_date'], errors='coerce')

# 2. 找出哪些列轉型失敗（clean_date 是 NaT，但原本的欄位不是空的）
dirty_data = df[df['clean_date'].isna() & df['last_active_date'].notna()]

# 3. 印出原本到底是哪些「髒字串」害 Pandas 沒辦法解析
print("被找出的非標準時間字串範例：")
print(dirty_data['last_active_date'].unique())





