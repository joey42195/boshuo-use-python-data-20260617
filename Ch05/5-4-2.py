# -*- coding: utf-8 -*-

"""
5-4-2事後檢定─找出真正的優勝方案
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

# =====================================================================
# 核心技術：執行 Tukey HSD 事後檢定 (Tukey's Honestly Significant Difference)
# =====================================================================
# endog: 因變數(連續型數據) -> 最終消費金額(元)
# groups: 自變數(類別型分組) -> 廣告版位設計
# alpha: 整體顯著水準，控制在 0.05
tukey_result = pairwise_tukeyhsd(endog=df['最終消費金額(元)'],
                                 groups=df['廣告版位設計'],
                                 alpha=0.05)

print("=" * 80)
print(" Tukey HSD 事後檢定報告：全組別兩兩對決安全驗證")
print("=" * 80)
print(tukey_result)
print("=" * 80 + "\n")

# =====================================================================
# 2. 繪製 Tukey HSD 置信區間圖 ──
# =====================================================================
# 建立畫布
fig, ax = plt.subplots(figsize=(10, 5))

# 繪製 Tukey HSD 信賴區間圖
tukey_result.plot_simultaneous(
    ax=ax,
    comparison_name='Layout_Blue',
    ylabel='廣告版位設計'
)

# 美化圖表與增添商業註解
ax.set_title('Tukey HSD 事後檢定：各廣告版位之平均客單價 95% 置信區間對照', fontsize=14, fontweight='bold')
ax.set_xlabel('最終消費金額(元) 估計值與安全邊界', fontsize=12)
ax.grid(True, alpha=0.3, linestyle=':')

plt.tight_layout()

plt.show()



