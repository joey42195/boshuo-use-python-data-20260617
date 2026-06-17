# -*- coding: utf-8 -*-

"""
5-4-1組間差異與組內波動
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# 設定繪圖風格與中文顯示
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 載入資料集
df = pd.read_csv("comprehensive_market_stats.csv")

# 2. 依「廣告版位設計」將最終消費金額分組
# 假設資料集內含 '紅、藍、綠' 或 'Design_A, Design_B, Design_C'
# 我們動態抓取獨特的版位名稱
layouts = df['廣告版位設計'].unique()
groups = [
    df[df['廣告版位設計'] == layout]['最終消費金額(元)']
    for layout in layouts
]

# 3. 計算各組的表面平均客單價，供後續商務對照
print("=" * 70)
print("各廣告版位設計之表面平均表現：")
for layout, group in zip(layouts, groups):
    print(
        f"【{layout}】平均消費: "
        f"{group.mean():.1f} 元 "
        f"(樣本數: {len(group)} 筆)"
    )
print("-" * 70)

# =====================================================================
# 核心技術：執行單因子方差分析 (One-way ANOVA)
# =====================================================================
f_stat, p_value = stats.f_oneway(*groups)

print(f"計算出的 F 統計量 (F-statistic): {f_stat:.4f}")
print(f"關鍵判定值 p值 (p-value): {p_value:.6f}")
print("-" * 70)



