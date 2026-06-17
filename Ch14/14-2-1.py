# -*- coding: utf-8 -*-

"""
14-2-1基準線—建立「如果沒有促銷」的參考座標
"""

import pandas as pd


# 基準線（Baseline）是數據分析師的「座標原點」。
# 在沒有第一月資料的情況下，我們無法判斷第二月的成長是來自促銷，還是市場本身就在增長。

# 1. 核心代碼實作：提取基準值
# 我們將使用第一月（1/1 ~ 1/30）這段「乾淨」的數據來定義什麼是常態。

# 載入資料 (確保使用 utf-8-sig 以處理中文亂碼問題)
df = pd.read_pickle('sales_basic_14_1_2.pkl')

#%%


# 1. 篩選出基準月（第一月）且屬於主機的資料
# 我們利用布林索引 (Boolean Indexing) 鎖定分析對象
baseline_data = df[
    (df['月份'] == '第一月(基準)') &
    (df['產品名稱'] == '咖啡機_主機')
]

# 2. 計算日平均銷量 (Daily Average Sales)
# mean() 函數能幫我們過濾每日的小幅波動，取得穩定的中心值
baseline_qty = baseline_data['銷量'].mean()

# 3. 計算基準毛利 (Baseline Profit)
# 先取得單件平均毛利，再乘以日均銷量，得出「不打折時」每天能賺多少錢
baseline_profit_per_unit = (
    baseline_data['單價']
    - baseline_data['成本']
).mean()

baseline_total_daily_profit = (
    baseline_qty
    * baseline_profit_per_unit
)
print(f"咖啡機_主機 基準日均銷量：{baseline_qty:.2f} 台")
print(f"咖啡機_主機 基準日均毛利：${baseline_total_daily_profit:.2f}")

