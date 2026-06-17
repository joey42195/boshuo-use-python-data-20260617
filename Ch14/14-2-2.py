# -*- coding: utf-8 -*-

"""
14-2-2增量業績計算—量化促銷活動的真實效果
"""

import pandas as pd


# 載入資料
df = pd.read_pickle('sales_basic_14_1_2.pkl')

#%%


# 13-2-2 增量業績 (Incremental Lift) 計算
# 有了基準線（約 50 台），我們就能計算第二月大促期間（2/11 ~ 2/17）到底帶來了多少「額外」的貢獻。

# 我們將大促期間的實際數據減去基準線。
baseline_qty = 50  # 基準線（約 50 台）

# 1. 篩選促銷期間主機資料
promo_period_data = df[
    (df['活動標籤'] == '大促期間') &
    (df['產品名稱'] == '咖啡機_主機')
]

# 2. 計算實際總銷量與預期總銷量 (基準 * 天數)
actual_promo_qty = promo_period_data['銷量'].sum()
expected_base_qty = baseline_qty * len(promo_period_data)

# 3. 計算純增量 (Incremental Lift)
incremental_lift_qty = (
    actual_promo_qty -
    expected_base_qty
)

lift_percentage = (
    incremental_lift_qty /
    expected_base_qty
) * 100

print(f"大促期間總銷量：{actual_promo_qty} 台")
print(f"預期自然銷量：{expected_base_qty:.2f} 台")
print(f"純增量業績：{incremental_lift_qty:.2f} 台 (成長率 {lift_percentage:.2f}%)")


#%%




