# -*- coding: utf-8 -*-

"""
14-2-3損益平衡點—這場仗打得值得嗎？
"""

import pandas as pd


# 載入資料
df = pd.read_pickle('sales_basic_14_1_2.pkl')

#%%


# 2. 損益平衡倍數的推導 (Break-even Multiple)
# 我們利用以下代碼來計算本次模擬數據中的「損益平衡門檻」：
# ---------------------------------------------------------
# 2. 損益平衡倍數的推導 (Break-even Multiple)
# 核心邏輯：計算銷量需要增加多少倍，才能補回因降價而損失的單位利潤。
# ---------------------------------------------------------

# 1. 定義基準獲利（未打折前的獲利結構）
unit_cost = 4000            # 設定產品成本（硬體成本通常固定）
original_price = 5000       # 設定原始售價
original_unit_profit = original_price - unit_cost  # 計算原單台毛利 (1000元)
baseline_qty = 50  # 基準線（約 50 台）

# 篩選促銷期間主機資料
promo_period_data = df[
    (df['活動標籤'] == '大促期間') &
    (df['產品名稱'] == '咖啡機_主機')
]


# 2. 定義促銷獲利（折扣後的獲利結構）
promo_price = 4000          # 設定促銷價（打 8 折後的價格）
promo_unit_profit = promo_price - unit_cost        # 計算折扣後的單台毛利 (0元)

# 3. 邏輯判斷與倍數計算
# 根據公式：損益平衡倍數 = 原單台毛利 / 促銷單台毛利
if promo_unit_profit <= 0:
    # 情況 A：若促銷價等於或低於成本，分母為 0 或負數，這意味著賣再多都無法回本
    be_multiple = float('inf') 
    print("警訊：打折後毛利為零或負值，單靠主機銷量無法達到損益平衡！")
else:
    # 情況 B：計算損益平衡所需達到的銷量倍數
    be_multiple = original_unit_profit / promo_unit_profit
    print(f"損益平衡倍數：{be_multiple:.2f} 倍")

#%%

# 實戰解讀—本次促銷成功了嗎？

promo_daily_avg = promo_period_data['銷量'].mean()
actual_multiple = promo_daily_avg / baseline_qty

print(f"實際銷量成長倍數：{actual_multiple:.2f} 倍")

if be_multiple == float('inf'):
    print("結論：主機毛利為零，無法僅靠銷量成長達成損益平衡。")
elif actual_multiple > be_multiple:
    print("結論：成功！銷量成長足以抵銷讓利。")
else:
    print("結論：失敗。雖然銷量增加，但總利潤低於不打折的情況。")



