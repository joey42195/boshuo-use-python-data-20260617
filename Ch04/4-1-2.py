
# -*- coding: utf-8 -*-

"""
4-1-2集中趨勢—平均數vs中位數
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# 設定繁體中文與負號支援
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# 1. 載入電商用戶行為資料集
df = pd.read_csv('eCommerceUser.csv')

# 2. 統計防線計算與繪製 (用視覺破解平均數的迷思)
mean_val = df['spending'].mean()
print(f"平均值是：{mean_val:.2f}")

median_val = df['spending'].median()
print(f"中位數值是：{median_val:.2f}")

# 加入眾數（.mode() 會回傳 Series，取 [0] 拿第一個，再四捨五入）
mode_val =df['spending'].mode()[0]
print(f"眾數值是：{mode_val:.2f}")

# 3. 初始化單張大畫布 (11x7 精準呈現長尾展開的黃金比例)
fig, ax = plt.subplots(figsize=(11, 7), facecolor='white')


# ==========================================
# 核心繪圖：直方圖與 KDE 曲線的完美融合
# ==========================================
# bins=50: 讓資料切分得更細緻，更容易看清長尾中的顆粒感
# kde=True: 疊加平滑的核密度估計曲線，勾勒數據的實體外觀
sns.histplot(
    data=df, x='spending', kde=True, ax=ax,
    color='#005088', bins=50, alpha=0.6, edgecolor='w',
    line_kws={'linewidth': 3, 'color': '#11caa0'}  # 亮色 KDE 線凸顯趨勢
)

# 繪製平均數線 (強烈紅色虛線)
ax.axvline(mean_val, color='#e74c3c', linestyle='--', linewidth=2.5, 
           label=f'算術平均數 (Mean): ${mean_val:,.0f}')
# 繪製中位數線 (穩健綠色實線)
ax.axvline(median_val, color='#27ae60', linestyle='-', linewidth=2.5, 
           label=f'數據中位數 (Median): ${median_val:,.0f}')

# 4. 圖表細節調校
ax.set_title("圖 4-1-2：電商用戶消費金額分布圖 (巨觀形狀診斷)\n核心任務：辨識右偏態與長尾效應 ── 破解平均數的遮羞布", 
             fontsize=14, weight='bold', color='#1a1a1a', pad=20)
ax.set_xlabel("年度累積消費金額 (Spending)", fontsize=11)
ax.set_ylabel("用戶人數 / 頻次 (Count)", fontsize=11)

# 優化千分位座標軸標籤
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
ax.grid(True, linestyle=':', alpha=0.4, color='#bdc3c7')
ax.legend(fontsize=11, loc='upper right')

plt.tight_layout()
plt.show()


