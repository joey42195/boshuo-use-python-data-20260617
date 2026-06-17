# -*- coding: utf-8 -*-

"""
14-5-2需求透支評估與活動排程—找回獲利的節奏
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

# 1. 偵測銷售凹陷 (Sales Dip)
# 我們要觀察大促結束後（2/18 之後）的市場反應。這是一個典型的「宿醉期」。
# 對比促銷後與基準線

# 1. 篩選促銷後觀察期資料 (2/18 - 2/28)
post_promo_data = df[(df['日期'] >= '2026-02-18') & (df['產品名稱'] == '咖啡膠囊_配件')]

# 2. 取得基準期 (第一月) 的日均銷量
base_qty_B = df[(df['月份'] == '第一月(基準)') & (df['產品名稱'] == '咖啡膠囊_配件')]['銷量'].mean()

# 3. 計算促銷後日均銷量
post_promo_avg = post_promo_data['銷量'].mean()

# 4. 計算凹陷程度
dip_percentage = (post_promo_avg - base_qty_B) / base_qty_B * 100



#%%

# 1. 計算「淨增量業績」 (Net Incremental Lift)
# 全週期增量結算
# 促銷期增量 (已在 14-2 算出)

incremental_lift_qty = 614
promo_lift_qty = 875

# 2. 促銷後凹陷流失量 (Post-Promo Loss)
# 比較促銷後 11 天與基準日均的差值總和
post_promo_actual_total = post_promo_data['銷量'].sum()
post_promo_expected_total = base_qty_B * len(post_promo_data)
post_promo_loss = post_promo_expected_total - post_promo_actual_total

# 3. 淨增量業績 (Net Incremental Lift)
net_lift = incremental_lift_qty - post_promo_loss

print(f"促銷期帳面增量：{incremental_lift_qty:.2f}")
print(f"促銷後預支損失：{post_promo_loss:.2f}")
print(f"全週期真實淨增量：{net_lift:.2f}")



