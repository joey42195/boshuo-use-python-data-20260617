# -*- coding: utf-8 -*-

"""
 6-2-2 同比 (YoY) — 基於精準模擬器的長期座標驗證
"""

import pandas as pd
import numpy as np

# 1. 載入售資料集
df = pd.read_csv("Store_Item_Demand_2024_2025.csv")


# 確保日期格式
df['date'] = pd.to_datetime(df['date'])


# =====================================================================
# 核心戰略 A：全站大盤的月同比（MoM vs YoY 雙軌診斷）
# =====================================================================

# 步驟一：先將全站每天的銷量聚合成「月度大盤」
df_monthly = df.groupby(['year', 'month'])['sales'].sum().reset_index()

# 創造一個月份字串 (如 "2024-01") 方便排版
df_monthly['月份'] = df_monthly['year'].astype(str) + '-' + df_monthly['month'].astype(str).str.zfill(2)
df_monthly = df_monthly.sort_values('月份').reset_index(drop=True)

# 步驟二：計算月環比 (MoM) ➔ 與「上個月(-1)」比
df_monthly['月環比(%)'] = (df_monthly['sales'].pct_change(1) * 100).round(1)

# 步驟三：計算月同比 (YoY) ➔ 與「去年同月(-12)」比
# 因為資料是一整年12個月垂直排列，所以 shift(12) 就能精準對齊去年同月！
df_monthly['去年同期銷量'] = df_monthly['sales'].shift(12)
df_monthly['月同比(%)'] = (df_monthly['sales'].pct_change(12) * 100).round(1)

print("\n【一、全站月度營運診斷報告】")
# 我們直接觀察 2025 年的表現（從第 12 筆資料開始，才有去年同期可比）
# 先用 .iloc 抓取特定列，再選取需要的欄位
target_rows = [12, 13, 19, 20, 23]
print(df_monthly.iloc[target_rows][['月份', 'sales', '月環比(%)', '去年同期銷量', '月同比(%)']].to_string(index=False))


# =====================================================================
# 核心戰略 B：細粒度交叉檢定（揪出 Item 5 的生命週期衰退）
# =====================================================================
print("\n" + "="*70)
print("【二、核心商品細分追蹤：Item 5（被淘汰商品）的年同比分析】")
print("="*70)

# 步驟一：按「商品」與「年份」聚合成年度總銷量
df_item = df.groupby(['item', 'year'])['sales'].sum().reset_index()

# 步驟二：利用 groupby('item') 鎖定商品，再用 shift(1) 抓取「該商品前一年」的銷量
# 確保 Item 1 的 2025 只會跟 Item 1 的 2024 比！
df_item['去年全年銷量'] = (
    df_item.groupby('item')['sales'].shift(1)
)

# 步驟三：計算年同比增長率 (YoY)
df_item['年同比(%)'] = ((df_item['sales'] - df_item['去年全年銷量']) / df_item['去年全年銷量'] * 100).round(1)

# # 過濾出 2025 年所有商品的年同比表現
# # 篩選出「2025 年」的資料
# # 因為年同比（YoY）需要與前一年比較，
# # 所以真正有商業分析價值的，通常是最新年度的結果
# df_item[df_item['year'] == 2025]

# # 選取要展示的重點欄位：
# # item               → 商品代號
# # 去年全年銷量        → 去年（2024）的總銷量
# # sales              → 今年（2025）的總銷量
# # 年同比(%)           → 年成長率（YoY）
# [['item', '去年全年銷量', 'sales', '年同比(%)']]

# # 將 sales 欄位重新命名為「今年全年銷量」
# # 讓報表更容易閱讀，也更符合商業語意
# .rename(columns={'sales': '今年全年銷量'})

# # 將 DataFrame 轉成純文字表格輸出
# # index=False 代表不顯示左側索引編號
# .to_string(index=False)

data = df_item[df_item['year'] == 2025][['item', '去年全年銷量', 'sales', '年同比(%)']].rename(columns={'sales': '今年全年銷量'}).to_string(index=False)
print(data)




