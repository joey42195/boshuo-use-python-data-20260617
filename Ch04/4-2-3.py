
# -*- coding: utf-8 -*-

"""
4-2-3類別vs數值—群組差異
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# 設定繁體中文與負號支援
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# 1. 載入電商用戶行為資料集
df = pd.read_csv('eCommerceUser.csv')

# 2.觀察數據：「平均值只是起點」
print("======= Step 1: 呼叫 groupby 進行多指標聚合 =======")
grouped_summary = df.groupby('user_type')['spending'].agg(['count', 'mean', 'median', 'std']).reindex(['VIP', 'Regular', 'Low'])
print(grouped_summary)

# 3. 初始化 1 列 2 行並排畫布 (16x7.5 黃金比例，實體書與簡報規格)
fig, axes = plt.subplots(1, 2, figsize=(16, 7.5), facecolor='white')


# 用於維持色彩一致性的調色盤
palette_dict = {'VIP': '#e74c3c', 'Regular': '#005088', 'Low': '#27ae60'}

# ==========================================
# 左圖 (A): 會員級別的平均消費額 (Barplot)
# ==========================================
# 模擬主管最愛的傳統圖表，內建 errorbar='ci' 展現信賴區間
sns.barplot(
    data=df, x='user_type', y='spending', ax=axes[0],
    order=['VIP', 'Regular', 'Low'], palette=palette_dict,
    errorbar='ci', alpha=0.8, edgecolor='#2c3e50', linewidth=1
)
axes[0].set_title("圖 A：各會員等級的「平均」消費金額 (表象)\n核心任務：觀察大眾視覺焦點，但警惕被單一均值誤導", 
                 fontsize=12, weight='bold', color='#005088', pad=15)
axes[0].set_xlabel("會員等級 (User Type)", fontsize=11)
axes[0].set_ylabel("平均消費金額 (Mean Spending)", fontsize=11)
axes[0].grid(True, linestyle=':', alpha=0.4)
axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"${int(x):,}"))

# ==========================================
# 右圖 (B): 會員消費的提琴圖分布 (Violin Plot)
# ==========================================
# 融合了「核密度估計」與「箱型圖」的精華，展示類別內部的結構真相
sns.violinplot(
    data=df, x='user_type', y='spending', ax=axes[1],
    order=['VIP', 'Regular', 'Low'], palette=palette_dict,
    inner='quartile', linewidth=2  # 顯示內部分佈的四分位數線
)
axes[1].set_title("圖 B：各會員等級的消費「提琴圖」分佈 (真相)\n核心任務：看穿厚度與長尾 ── 揪出群體內部的行為異質性", 
                 fontsize=12, weight='bold', color='#11caa0', pad=15)
axes[1].set_xlabel("會員等級 (User Type)", fontsize=11)
axes[1].set_ylabel("實際消費金額分佈 (Spending Distribution)", fontsize=11)
axes[1].set_ylim(-10000, 150000) # 適度調整 Y 軸範圍，讓主體提琴形狀更清晰
axes[1].grid(True, linestyle=':', alpha=0.4)
axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"${int(x):,}"))

# 4. 頂部總標題絕對定位 (無銀河留白規範)
fig.text(0.5, 0.95, "類別變數 vs 數值變數：用統計聚合與提琴圖擊穿「平均數」的迷思", 
         ha='center', fontsize=16, fontweight='bold', color='#2c3e50')

plt.tight_layout()
plt.subplots_adjust(top=0.86)

# plt.savefig("4-2-3.png", dpi=300, bbox_inches='tight')
# print("🎉 4-2-3 類別與數值群組差異圖已成功輸出：4-2-3_category_vs_numerical_differences.png")
plt.show()

