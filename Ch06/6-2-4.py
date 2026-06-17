# -*- coding: utf-8 -*-

"""
 6-2-4 複合增長率 (CAGR) — 五年期零售大盤長線定海神針實作
"""

import pandas as pd
import numpy as np

# 1. 載入資料集
df = pd.read_csv("Store_Item_Demand_2021_2025.csv")

# =====================================================================
# 2. 資料變形：將「日流水帳」轉化為「商品 x 年份」的年度總銷量表
# =====================================================================
# 利用 groupby 聚合各商品每年的總銷量
df_yearly = df.groupby(['item', 'year'])['sales'].sum().reset_index()


# 利用 pivot 矩陣化，讓年份變成欄位，這樣起點(2021)與終點(2025)一目了然
# 將「長表（Long Format）」轉換為「寬表（Wide Format）」
# index='item'   每一列(Row)代表一個商品(item)
# columns='year' 將年份(year)展開成欄位(Column)
# values='sales'  欄位中的數值使用該商品該年的總銷量(sales)
df_pivot = (
    df_yearly
    .pivot(index='item', columns='year', values='sales')
    .reset_index()
)


# =====================================================================
# 3. 核心技術：動態計算 5 年複合年度成長率 (CAGR)
# =====================================================================
# 定義計算期數 n (2025 - 2021 = 4 期)
n_periods = 2025 - 2021

# 套用 CAGR 核心公式： (Ending / Beginning) ** (1/n) - 1
df_pivot['5年總增長倍數'] = (df_pivot[2025] / df_pivot[2021]).round(2)
# CAGR 運算（注意 -1 外面的小括號）
df_pivot['5年CAGR(%)'] = ((((df_pivot[2025] / df_pivot[2021]) ** (1 / n_periods)) - 1) * 100).round(1)

# 為了對照，我們補上「4年同比算術平均數」
# 先算各年度的單年同比 (YoY)
df_pivot['22_YoY'] = (df_pivot[2022] - df_pivot[2021]) / df_pivot[2021]
df_pivot['23_YoY'] = (df_pivot[2023] - df_pivot[2022]) / df_pivot[2022]
df_pivot['24_YoY'] = (df_pivot[2024] - df_pivot[2023]) / df_pivot[2023]
df_pivot['25_YoY'] = (df_pivot[2025] - df_pivot[2024]) / df_pivot[2024]

# 算術平均
df_pivot['單年同比算術平均(%)'] = ((df_pivot[['22_YoY', '23_YoY', '24_YoY', '25_YoY']].mean(axis=1)) * 100).round(1)

# =====================================================================
# 4. 輸出最終商務決策矩陣
# =====================================================================
report_cols = ['item', 2021, 2025, '5年總增長倍數', '單年同比算術平均(%)', '5年CAGR(%)']
print("【五大商品：五年長期 CAGR 戰略決策矩陣】")
print(df_pivot[report_cols].to_string(index=False))