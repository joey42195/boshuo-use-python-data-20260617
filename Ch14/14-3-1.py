# -*- coding: utf-8 -*-

"""
14-3-1關聯性檢驗—主機真的帶動配件嗎？
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 載入資料
df = pd.read_pickle('sales_basic_14_1_2.pkl')


#%%

# 利用 Pearson 相關係數驗證連動性我們透過相關係數 r 來衡量「主機銷量」與「膠囊銷量」的線性關係。

# 將每日銷量整理成寬表
pivot_df = (
    df.pivot_table(
        index='日期',
        columns='產品名稱',
        values='銷量'
    )
    .fillna(0)
)

# 計算相關係數
r_value = (
    pivot_df[['咖啡機_主機', '咖啡膠囊_配件']]
    .corr()
    .iloc[0, 1]    # 咖啡機與膠囊之間的相關係數
)
print(f"主機與配件相關係數：{r_value:.4f}")  # 0.9909


# 相關係數雖然精確，但有時會被「離群值」欺騙。
# 因此，分析師一定會繪製散佈圖，親眼確認這條「連動線」的健康狀況。

plt.figure(figsize=(8, 6))
sns.regplot(data=pivot_df, x='咖啡機_主機', y='咖啡膠囊_配件', 
            scatter_kws={'alpha':0.5}, line_kws={'color':'red'})

plt.title(f'主機 vs. 配件銷量散佈圖 (r = {r_value:.2f})')
plt.xlabel('主機銷量')
plt.ylabel('配件銷量')
plt.grid(True, linestyle='--', alpha=0.6)

plt.show()


#%%


# 領先指標與滯後相關 (Lagged Correlation)
# 實務上，消費者買了咖啡機後，通常會先使用附贈的試用膠囊，2 到 3 天後才會開始購買新的膠囊。
# 這就是所謂的「滯後效應」。

# ---------------------------------------------------------
# 核心邏輯：驗證「今天買主機」是否會帶動「兩天後」的配件銷售。
# ---------------------------------------------------------

# 1. 建立滯後變數 (Lag Variable)
# 使用 shift(-2) 將配件銷量的數據「向上平移」兩天
# 這意味著將 5/3 的配件銷量，對齊到 5/1 的主機銷量上
pivot_df['膠囊_滯後2天'] = pivot_df['咖啡膠囊_配件'].shift(-2)

# 2. 計算滯後相關係數
# 比較「當日主機銷量」與「兩天後配件銷量」的線性關係
# correlation_matrix 會得到 2x2 矩陣，我們取出 [0, 1] 位置的係數值
lagged_corr = pivot_df[['咖啡機_主機', '膠囊_滯後2天']].corr().iloc[0, 1]

print(f"主機與配件（滯後 2 天）的相關係數：{lagged_corr:.4f}")


# 如果滯後相關係數高於當日相關係數，這就證明了主機銷量是配件需求的領先指標。

