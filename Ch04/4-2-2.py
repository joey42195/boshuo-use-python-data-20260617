# -*- coding: utf-8 -*-

"""
4-2-2散點圖中的模式
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# 設定繁體中文與負號支援
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# 1. 載入電商用戶資料集 (請替換為你的實際檔案路徑)
df = pd.read_csv("eCommerceUser.csv")
df.columns

# 篩選出你真正感興趣的 4~6 個核心營運指標
# 特別注意「維度災難」
df_pair = df[['user_type', 'income', 'visits', 'spending']]
# 設定繁體中文與負號支援
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# 2. 定義用戶分群的專屬商務色彩
user_colors = {
    'VIP': '#9b59b6',      # 高雅紫 (預留給可能有VIP的完整資料)
    'Regular': '#3498db',  # 專業藍
    'Low': '#e67e22'       # 警示橘
}

# 3.使用 Seaborn 的 pairplot 建立「配對圖（Scatterplot Matrix）」
# diag_kind='kde'：對角線顯示機率密度圖（看單一變數分佈）
# plot_kws：控制非對角線散點的透明度與邊框，讓大量數據重疊時依然清晰
grid = sns.pairplot(
    data=df_pair,    # 指定資料來源 DataFrame
    # hue='user_type'
    # 根據 user_type 欄位進行分類上色
    # 不同客群（VIP / Regular / Low）會使用不同顏色
    hue='user_type',
    palette=user_colors,    # 指定各客群的顏色配置

    # diag_kind='kde'
    # 對角線顯示 KDE（核密度估計）分布圖
    # 用來觀察單一變數本身的分布形狀
    diag_kind='kde',    # 對角線顯示 KDE（核密度估計）分布圖

    # plot_kws：設定非對角線散點圖的樣式
    plot_kws={

        # alpha=0.6
        # 設定透明度
        # 避免大量資料點重疊時太擁擠
        'alpha': 0.6,        # alpha=0.6

        # 提升資料點辨識度
        'edgecolor': 'white',        # 為散點加上白色邊框
        's': 40        # 設定散點大小（size）
    }
)

# 4. 圖表商務美學優化
# 為整體矩陣圖加上主標題，並精準預留頂部空間避免壓到圖表
grid.fig.suptitle(
    "電商用戶多維特徵配對圖 (Pair Plot)\n戰略任務：一次揭露「特徵兩兩關聯」與「用戶分群生態」", 
    fontsize=16, fontweight='bold', color='#2c3e50', y=1.02
)

# 觸發圖例優化（調整到舒適的位置）
sns.move_legend(grid, "upper left", bbox_to_anchor=(1, 1), title="用戶類別")

plt.show()