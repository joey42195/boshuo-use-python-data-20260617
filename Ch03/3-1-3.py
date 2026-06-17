# -*- coding: utf-8 -*-

"""
3-1-3三大套件繪製直方圖比較
"""


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 設定繁體中文與負號正常顯示
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False


# 1. 載入資料並篩選出 Store 1 的營運數據
df = pd.read_csv("Store_Item_Demand.csv")
store1_df = df[df['store'] == 1].copy()


# ==========================================
# Pandas 內建繪圖
# ==========================================
# 建立圖表畫布大小（寬 6、高 4），figsize 單位為英吋 (inch)
plt.figure(figsize=(6, 4))

# 使用 Pandas 內建 plot() 快速繪製直方圖
# kind='hist' 代表圖表類型為 Histogram（直方圖）
# bins=20 表示將資料切成 20 個區間
# color='skyblue' 設定長條顏色為天藍色
# edgecolor='black' 為每個長條加上黑色邊框，提升可讀性
store1_df['sales'].plot(
    kind='hist',     # 指定圖表類型為直方圖
    bins=20,    # 將資料切成 20 個區間
    color='skyblue',      # 長條顏色
    edgecolor='black'    # 長條邊框顏色
)

# 設定圖表標題
plt.title("Pandas 內建快速直方圖 (EDA 專用)")

# 設定 X 軸標題
plt.xlabel("每日銷量")

# 設定 Y 軸標題
plt.ylabel("頻率")

# 顯示圖表
plt.show()

# ==========================================
# Matplotlib 繪圖
# ==========================================
plt.figure(figsize=(6, 4))
# 使用底層引擎的 plt.hist()，並手工雕琢每一個視覺元素
plt.hist(
    store1_df['sales'],      # 繪圖數據：指定要分析的欄位為 1 號分店的「銷售額(sales)」
    bins=20,                 # 分箱數量：將銷售額數據由小到大「平分成 20 個區間（直條）」
    color='#2c3e50',         # 直條顏色：使用深藍灰色（HEX 碼），提升圖表的高級感與商務質感
    edgecolor='white',       # 邊框顏色：直條之間加上「白色外框」，讓每個區間邊界更清晰、不糊成一片
    alpha=0.9                # 透明度：設定為 90%（1 為完全不透明），微調視覺視覺，讓圖表看起來更輕盈
)
plt.title("Matplotlib 畫布精雕直方圖 (客製化專用)", fontsize=12, fontweight='bold')
plt.xlabel("每日銷量 (Sales)", fontsize=10)
plt.ylabel("天數統計 (Count)", fontsize=10)
plt.grid(True, linestyle='--', alpha=0.5) # 手工加上網格
# 顯示圖表
plt.show()

# ==========================================
# Seaborn 繪圖
# ==========================================
plt.figure(figsize=(6, 4))
# 使用高階統計函數，一鍵附贈 KDE 趨勢曲線與高質感配色
sns.histplot(
    data=store1_df,       # 指定資料來源：要繪製的 DataFrame 為 store1_df
    x='sales',            # 指定 X 軸欄位：將「銷售額(sales)」數據拿來做分佈分析
    bins=20,              # 分箱數量：將銷售額數據範圍「平分成 20 個數據區間（直條）」
    color='#e74c3c',      # 圖表主色：使用鮮豔的「猩紅色/亮紅色」（HEX 碼），視覺效果非常搶眼
    kde=True,             # 核心密度估計：加入平滑的「機率密度曲線」，用來輔助觀察數據的連續分佈趨勢
    edgecolor='black'     # 邊框顏色：直條外框加上「黑色邊線」，與紅色直條形成強烈對比、邊界更鮮明
)
plt.title("Seaborn 高級統計直方圖 (簡報與報告專用)", fontsize=12)
plt.xlabel("每日銷量")
plt.ylabel("計數")
plt.show()




#%%


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 載入資料並篩選出 Store 1 的營運數據
df = pd.read_csv("Store_Item_Demand.csv")
store1_df = df[df['store'] == 1].copy()

# 2. 初始化高階並排畫布：1 列 3 行 (1 Row, 3 Columns)
# figsize 寬度設為 18、高度設為 5，這是黃金比例，能確保每張圖都不會被擠壓變形
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 設定全球統一的繁體中文與負號支援
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# ==========================================
# 子圖一 (左)：Pandas 內建快速直方圖
# ==========================================
# 核心技術：利用 ax=axes[0]，強行將 Pandas 的圖指定畫在第一個格子
store1_df['sales'].plot(kind='hist', bins=20, color='skyblue', edgecolor='black', ax=axes[0])
axes[0].set_title("Pandas 內建快速直方圖\n(特點：兩行代碼、探索極快)", fontsize=12, weight='bold', pad=10)
axes[0].set_xlabel("每日銷量")
axes[0].set_ylabel("頻率")

# ==========================================
# 子圖二 (中)：Matplotlib 底層客製直方圖
# ==========================================
# 核心技術：使用 axes[1].hist()，在第二個格子進行純手工細節精雕
axes[1].hist(store1_df['sales'], bins=20, color='#2c3e50', edgecolor='white', alpha=0.9)
axes[1].set_title(" Matplotlib 畫布精雕直方圖\n(特點：底層控制、極致客製)", fontsize=12, weight='bold', pad=10)
axes[1].set_xlabel("每日銷量 (Sales)")
axes[1].set_ylabel("天數統計 (Count)")
axes[1].grid(True, linestyle='--', alpha=0.5) # 手工刻上精細網格

# ==========================================
# 子圖三 (右)：Seaborn 高階統計直方圖
# ==========================================
# 核心技術：利用 ax=axes[2]，將高顏值的 Seaborn 統計圖指定送入第三個格子
sns.histplot(data=store1_df, x='sales', bins=20, color='#e74c3c', kde=True, edgecolor='black', ax=axes[2])
axes[2].set_title("Seaborn 高級統計直方圖\n(特點：自帶曲線、簡報擔當)", fontsize=12, weight='bold', pad=10)
axes[2].set_xlabel("每日銷量")
axes[2].set_ylabel("計數")

# 3. 終極排版優化：防止三個子圖的軸標籤和標題相互打架、重疊
plt.tight_layout()

# 4. 輸出高品質的教科書並排插圖
# plt.savefig("4-1-3.png", dpi=300, bbox_inches='tight')
# print("驚豔的『三位一體並排對比圖』已儲存為：visualization_battle_row.png")
plt.show()



