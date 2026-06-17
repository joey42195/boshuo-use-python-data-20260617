# -*- coding: utf-8 -*-

"""
1-3-1資料讀取與寫入
"""

import pandas as pd


# ==========================================
# 1-2-1 資料寫入與讀取 (模擬示範)
# ==========================================

# 讀取 CSV 資料檔
# 將 mock_orders.csv 載入成 DataFrame 物件
df = pd.read_csv('mock_orders.csv')

# 顯示讀取後的資料內容
print(df)

# 將 DataFrame 寫出為 CSV 檔案
# index=False 表示不輸出索引欄位
# encoding="utf-8-sig" 可避免 Excel 開啟中文時出現亂碼
df.to_csv("mock_orders_01.csv", index=False, encoding="utf-8-sig")

# 將 DataFrame 儲存為 Pickle 格式
# Pickle 可完整保留資料型態與 DataFrame 結構
df.to_pickle("mock_orders.pkl")

# 重新讀取剛剛輸出的 CSV 檔案
df_csv = pd.read_csv("mock_orders_01.csv")

# 顯示重新讀取的 CSV 資料
print(df_csv)

# 重新讀取 Pickle 檔案
df_pkl = pd.read_pickle("mock_orders.pkl")

# 顯示重新讀取的 Pickle 資料
print(df_pkl)