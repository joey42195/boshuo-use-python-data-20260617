# -*- coding: utf-8 -*-

"""
14-3-2促銷投資效益分析—從引流成本到整體損益評估
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 載入資料
df = pd.read_pickle('sales_basic_14_1_2.pkl')


# 跨產品損益平衡分析 (Cross-Product Break-even)
# 我們要建立一個複合模型，將主機的「讓利損失」視為一種行銷投資，而將配件的「增量利潤」視為投資回報。

# 計算淨影響 (Net Impact)

# 1. 計算主機讓利虧損 (A)
# 大促期間主機單價由 5000 降至 4000
promo_qty_A = df[(df['活動標籤'] == '大促期間') & (df['產品名稱'] == '咖啡機_主機')]['銷量'].sum()
loss_A = (5000 - 4000) * promo_qty_A

# 2. 計算配件附帶收益 (B)
# 先取得配件基準日均銷量
base_qty_B = df[(df['月份'] == '第一月(基準)') & (df['產品名稱'] == '咖啡膠囊_配件')]['銷量'].mean()
promo_data_B = df[(df['活動標籤'] == '大促期間') & (df['產品名稱'] == '咖啡膠囊_配件')]

# 配件增量 = 促銷期實際銷量 - (基準日均 * 促銷天數)
incremental_qty_B = promo_data_B['銷量'].sum() - (base_qty_B * len(promo_data_B))
# 配件單位毛利 = 500 - 100 = 400
profit_B = incremental_qty_B * 400

# 3. 淨影響計算
net_impact = profit_B - loss_A

print(f"主機讓利總額：${loss_A:,.0f}")
print(f"配件帶來之附帶增量毛利：${profit_B:,.0f}")
print(f"促銷活動對品類總 P&L 的淨影響：${net_impact:,.0f}")






