
"""
5-1-1隨機性與資料分布
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 設定繪圖風格與中文顯示
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 載入我們的全功能統計資料集
df = pd.read_csv("comprehensive_market_stats.csv")

# =====================================================================
# 盲點實驗：如果我們不檢查分佈，直接看「平均值」...
# =====================================================================
mean_A = df[df['AB測試分組'] == 'Group_A']['最終消費金額(元)'].mean()
mean_B = df[df['AB測試分組'] == 'Group_B']['最終消費金額(元)'].mean()

print("=" * 70)
print("【只看平均值的匯報】")
print("=" * 70)
print(f"Group_A (舊版流程) 的平均客單價: {mean_A:.1f} 元")
print(f"Group_B (新版流程) 的平均客單價: {mean_B:.1f} 元")
print("=" * 70 + "\n")

# =====================================================================
# 撕開表象，檢查兩組的數據「分佈型態」與中位數
# =====================================================================
median_A = df[df['AB測試分組'] == 'Group_A']['最終消費金額(元)'].median()
median_B = df[df['AB測試分組'] == 'Group_B']['最終消費金額(元)'].median()

print("=" * 70)
print("【撕開分佈型態的真相】")
print("=" * 70)
print(f"Group_A (舊版流程) 的中位數 (Median): {median_A:.1f} 元")
print(f"Group_B (新版流程) 的中位數 (Median): {median_B:.1f} 元")
print("=" * 70 + "\n")

# =====================================================================
# 視覺化對照：畫出兩組的分佈
# =====================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
plt.suptitle('5-1-1 商業實驗診斷：為什麼平均值會說謊？', fontsize=16, fontweight='bold')

# 左圖：Group_A 的分佈
sns.histplot(data=df[df['AB測試分組'] == 'Group_A'], x='最終消費金額(元)', bins=50, color='#1f77b4', ax=ax1, kde=True)
ax1.axvline(mean_A, color='red', linestyle='--', linewidth=2, label=f'平均數: {mean_A:.1f}')
ax1.axvline(median_A, color='green', linestyle='-', linewidth=2, label=f'中位數: {median_A:.1f}')
ax1.set_title("Group_A (舊版流程) 數據分佈")
ax1.set_xlim(500, 3000) # 限制視角以便觀察主體
ax1.legend()

# 右圖：Group_B 的分佈
sns.histplot(data=df[df['AB測試分組'] == 'Group_B'], x='最終消費金額(元)', bins=50, color='#ff7f0e', ax=ax2, kde=True)
ax2.axvline(mean_B, color='red', linestyle='--', linewidth=2, label=f'平均數: {mean_B:.1f}')
ax2.axvline(median_B, color='green', linestyle='-', linewidth=2, label=f'中位數: {median_B:.1f}')
ax2.set_title("Group_B (新版流程) 數據分佈")
ax2.set_xlim(500, 3000)
ax2.legend()

plt.tight_layout()

plt.show()