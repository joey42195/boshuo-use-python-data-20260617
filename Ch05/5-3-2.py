# -*- coding: utf-8 -*-

"""
5-3-2 t檢定與雙組比較
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

# 2. 抽取 Group_A（舊版流程）與 Group_B（新版流程）的消費金額數據
group_A_revenue = df[df['AB測試分組'] == 'Group_A']['最終消費金額(元)']
group_B_revenue = df[df['AB測試分組'] == 'Group_B']['最終消費金額(元)']

# 3. 計算表面上的商務指標
mean_A = group_A_revenue.mean()
mean_B = group_B_revenue.mean()
diff = mean_B - mean_A

# =====================================================================
# 核心技術：執行雙獨立樣本 t 檢定 (Two-Sample t-test)
# =====================================================================
# 使用 stats.ttest_ind，並設定 equal_var=False (採用 Welch's t-test，更符合現實中兩組變異數不同的狀況)
t_stat, p_value = stats.ttest_ind(
    group_B_revenue,
    group_A_revenue,
    equal_var=False
)


print("=" * 70)
print("5-3-2 雙獨立樣本 t 檢定報告：A/B 測試最終決策")
print("=" * 70)
print(f"Group_A (舊版流程) 平均客單價: {mean_A:.2f} 元 (樣本數: {len(group_A_revenue)} 筆)")
print(f"Group_B (新版流程) 平均客單價: {mean_B:.2f} 元 (樣本數: {len(group_B_revenue)} 筆)")
print(f"表面數據差距 (B - A): {diff:+.2f} 元")
print("-" * 70)
print(f"計算出的 t 統計量 (t-statistic): {t_stat:.4f}")
print(f"關鍵判定值 p值 (p-value): {p_value:.6f}")
print("-" * 70)

# 商業決策邏輯判定
alpha = 0.05
if p_value < alpha:
    print("最終商務決策：【高度顯著，批准上線！】")
    print(f"   原因：p值遠小於 {alpha}。這代表新流程帶來的 {diff:.2f} 元增長，")
else:
    print("最終商務決策：【不顯著，維持原狀！】")
    print(f"   原因：p值大於 {alpha}。雖然表面上新流程高了 {diff:.2f} 元，")
    print("            但在統計上，這個差距有很高機率只是隨機的『運氣噪音』。")


#%%

# =====================================================================
# 核心技術：計算兩組平均數差值的 95% 信心區間 (Welch-Satterthwaite 自由度)
# =====================================================================

# Welch's t-test（不假設兩組變異數相同）
result = stats.ttest_ind(
    group_B_revenue,
    group_A_revenue,
    equal_var=False
)

# 取得 t 值與 p 值
t_stat = result.statistic
p_value = result.pvalue

# 直接取得 95% 信心區間
ci = result.confidence_interval(confidence_level=0.95)

# 信心區間上下界
ci_lower = ci.low
ci_upper = ci.high

# 平均差異
diff = group_B_revenue.mean() - group_A_revenue.mean()

print(f"t值: {t_stat:.4f}")
print(f"p值: {p_value:.6f}")
print(f"平均差異: {diff:.2f} 元")
print(f"95% 信心區間: [{ci_lower:.2f}, {ci_upper:.2f}]")






