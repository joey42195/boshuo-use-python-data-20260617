# -*- coding: utf-8 -*-

"""
5-4-3效果量—顯著不等於重要
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# 設定繪圖風格與中文顯示
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 載入資料集
df = pd.read_csv("comprehensive_market_stats.csv")
df.columns


import pingouin as pg

group_A_revenue = df[df['AB測試分組'] == 'Group_A']['最終消費金額(元)']
group_B_revenue = df[df['AB測試分組'] == 'Group_B']['最終消費金額(元)']

# 計算 Cohen's d
effect_size = pg.compute_effsize(
    group_B_revenue,
    group_A_revenue,
    eftype='cohen'
)

print(f"Cohen's d: {effect_size:.3f}")


#%%

import pingouin as pg

# 單因子變異數分析（One-way ANOVA）
anova_result = pg.anova(
    
    # 輸入的資料表（DataFrame）
    data=df,
    
    # dv（Dependent Variable）
    # 因變數／連續型數值欄位
    # 這裡代表「要比較的指標」：最終消費金額
    dv='最終消費金額(元)',
    
    # between
    # 組別變數／類別型欄位
    # 這裡代表不同的廣告版位設計（Blue、Red、Green）
    between='廣告版位設計',
    
    # detailed=True
    # 顯示完整 ANOVA 統計表
    # 包含 SS、DF、MS、F、p-value、效果量等資訊
    detailed=True
)

print(anova_result)





