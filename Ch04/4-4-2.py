# -*- coding: utf-8 -*-

"""
4-4-1類別分布—誰最多？
"""

import numpy as np
import pandas as pd

df = pd.read_csv('eCommerceUser.csv')

# ---------------------------------------------------------------------
# 【4-4-2 群體差異】不同群行為不同嗎？撕開平均值的偽裝
# ---------------------------------------------------------------------

# 依照 user_type（會員類型）進行分組
# 並同時計算 spending 與 conversion_rate 的統計摘要

behavior_matrix = (df.groupby('user_type')[['spending', 'conversion_rate']]               # 選取要分析的欄位
    .agg([
        'mean',             # 平均值
        'median'            # 中位數
    ])
)

# 顯示結果
behavior_matrix
print(behavior_matrix.round(4))


