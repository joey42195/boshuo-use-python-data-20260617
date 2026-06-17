# -*- coding: utf-8 -*-

"""
1-3-3資料選取
"""

import pandas as pd

# 讀取資料
df = pd.read_csv('mock_orders.csv')
df.columns

# ==========================================
# 1-3-3 資料選取
# ==========================================

data01 = df[['Name']]  #選取Name欄位
print(data01)

data02 = df[['Name', 'Age']]  #選取Name、Score兩欄
print(data02)


# 列資料選取(Slicing)

df.loc[0]  # 選取名稱為 0 的第 1 列(或使用 df.iloc[0])
df.loc[0:3]  # 選取 0~3 列。注意：loc 參數值「含頭也含尾」
df.iloc[0:3]  # 選取位置為 0~2 的列。注意：iloc 參數值「含頭不含尾」
df.iloc[-5:]  # 取出最後 5 筆資料(負索引代表由後往前計數)

