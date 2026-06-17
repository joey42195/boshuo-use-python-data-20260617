# -*- coding: utf-8 -*-

"""
14-4-2品類淨利潤評估—警惕利潤空洞化
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

# 1. 整體品類毛利的加總邏輯
# 我們不能孤立地看產品。分析師必須將這 60 天內所有受影響的產品利潤加總，才能得出這場促銷的「真面目」。

# 1. 定義品類產品清單
category_products = ['咖啡機_主機', '咖啡膠囊_配件', '他牌_競品']

# 2. 計算基準期 (第一月) 的日均總利潤
baseline_total_profit = df[df['月份'] == '第一月(基準)']['利潤'].sum() / 30

# 3. 計算大促期間 (2/11 - 2/17) 的日均總利潤
promo_total_profit = df[df['活動標籤'] == '大促期間']['利潤'].sum() / 7

# 4. 比較變動
profit_diff = promo_total_profit - baseline_total_profit
profit_growth_rate = (profit_diff / baseline_total_profit) * 100

print(f"基準期品類日均總利潤：${baseline_total_profit:,.0f}")
print(f"大促期品類日均總利潤：${promo_total_profit:,.0f}")
print(f"品類總利潤變動率：{profit_growth_rate:.2f}%")






