
# -*- coding: utf-8 -*-

"""
2-1-3型別錯誤與轉換問題
"""

import pandas as pd
import numpy as np

# 1. 載入數據
df = pd.read_csv('E-commerce_Dirty_Dataset.csv')
df.info()
# ---------------------------------------------------------------------
# 為什麼盲目使用 .astype() 會直接炸裂？
# ---------------------------------------------------------------------
print("\n如果我們對含有髒字串的數值欄位盲目使用 .astype()...")

# 觀察錯誤後，請註解此行
df['spending'].astype(int)  # 這行會報錯

try:     # 轉型時，最好使用例外偵測
    # 嘗試強行將含有 文字 的欄位轉為 數值
    df['spending'].astype(int)
except Exception as e:
    print(f"系統報錯！錯誤訊息為: {e}")


# ---------------------------------------------------------------------
# 數值欄位的安全轉換 (pd.to_numeric)
# ---------------------------------------------------------------------
print("\n" + "-" * 70)
print(" 安全轉換 .. 使用 pd.to_numeric + errors='coerce' 處理數值欄位")
print("-" * 70)

# 在轉型前，我們先看看 spending 欄位原本的型態（讀取時可能被誤判或夾雜文字）
print(f"轉換前 spending 的欄位型態: {df['spending'].dtype}")

# 安全轉換：遇到無法轉換的雜訊，強制化為 NaN，而不會報錯中斷
spending_clean = pd.to_numeric(df['spending'], errors='coerce')

print(f"轉換後 spending 的欄位型態: {spending_clean.dtype}")
print(f"成功轉為浮點數！因型別不合被迫現形的缺失值數量: {spending_clean.isnull().sum()} 筆")



