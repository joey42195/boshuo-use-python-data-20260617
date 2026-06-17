# -*- coding: utf-8 -*-

"""
14-5-1囤貨效應辨識—消失的訂單只是被提前了
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

print(f"配件基準日均銷量：{base_qty_B:.2f}")
print(f"促銷後日均銷量：{post_promo_avg:.2f}")
print(f"銷售凹陷幅度：{dip_percentage:.2f}%")




