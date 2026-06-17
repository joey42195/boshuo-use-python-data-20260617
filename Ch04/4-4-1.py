# -*- coding: utf-8 -*-

"""
4-4-1類別分布—誰最多？
"""

import numpy as np
import pandas as pd

df = pd.read_csv('eCommerceUser.csv')

# ---------------------------------------------------------------------
# 4-4-1 類別分布—誰最多？
# ---------------------------------------------------------------------
print("\n 類別分布 大盤先天用戶等級比例：")
user_ratio = df['user_type'].value_counts(normalize=True) * 100
user_counts = df['user_type'].value_counts()

# 合併人數與百分比，建立清晰的結構表格
df_441 = pd.DataFrame({'絕對人數 (人)': user_counts, '相對佔比 (%)': user_ratio.round(2)})
print(df_441)

