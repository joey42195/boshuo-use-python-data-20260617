
"""
5-2-2樣本量與估計精度
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 設定繪圖風格與中文顯示
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 載入我們的資料集
df = pd.read_csv("comprehensive_market_stats.csv")

# 2. 以全站 12,730 筆訂單的平均消費金額作為「母體平均值」
true_mean = df['最終消費金額(元)'].mean()

# 3. 模擬不同樣本量下的估算精準度
sample_sizes = [10, 20, 50, 100, 200, 500, 1000, 1500, 2000, 3000]
errors = []

np.random.seed(42)  # 固定隨機種子，確保結果完全可重現

for n in sample_sizes:
    trial_errors = []
    for _ in range(50):
        sample_mean = df['最終消費金額(元)'].sample(n, replace=False).mean()
        trial_errors.append(abs(sample_mean - true_mean))
    errors.append(np.mean(trial_errors))

# 4. 繪製商業邊際收益遞減曲線
plt.figure(figsize=(11, 6))
plt.plot(sample_sizes, errors, marker='o', linestyle='-', color='#2980b9', linewidth=2.5, label='平均估算誤差')
plt.fill_between(sample_sizes, errors, color='#3498db', alpha=0.1)

# 動態抓取誤差值
err_100 = errors[sample_sizes.index(100)]
err_2000 = errors[sample_sizes.index(2000)]

# =====================================================================
# 繪圖
# =====================================================================

# 標註點一：n=100 的黃金拐點
plt.annotate('誤差斷崖式下跌！\n(C/P值極高)', 
             xy=(100, err_100), 
             xytext=(350, err_100 + 40),  # 修正垂直距離，不讓文字飛太遠
             fontsize=11,
             fontweight='bold',
             arrowprops=dict(facecolor='black',                              
                             edgecolor='black',
                             shrink=0.1, 
                             width=1, 
                             headwidth=6, 
                             headlength=6,
                             connectionstyle="arc3,rad=-0.1")) # 帶有一點點優雅弧度的箭頭

# 標註點二：n=2000 的平緩區
plt.annotate('進入邊際收益遞減區\n(多花錢卻買不到更多精準度)', 
             xy=(2000, err_2000), 
             xytext=(1300, err_2000 + 50), # 修正垂直距離，使其與資料點完美對齊
             fontsize=11,
             fontweight='bold',
             arrowprops=dict(facecolor='crimson', 
                             edgecolor='crimson',
                             shrink=0.1, 
                             width=1, 
                             headwidth=6, 
                             headlength=6,
                             connectionstyle="arc3,rad=0.1"))

plt.title('5-2-3 樣本量設計照妖鏡：樣本數 (n) 與估算誤差的邊際收益遞減曲線', fontsize=15, fontweight='bold')
plt.xlabel('隨機抽樣的樣本數量 / 問卷回收量 (Sample Size n)', fontsize=12)
plt.ylabel('平均絕對誤差 (與真實客單價的距離/元)', fontsize=12)
plt.grid(True, alpha=0.4, linestyle=':')
plt.legend(fontsize=11)
plt.tight_layout()


plt.show()
