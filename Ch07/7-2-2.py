# -*- coding: utf-8 -*-

"""
7-2-2實作範例—商品貢獻度分析
"""

import pandas as pd
import numpy as np

# 1. 載入資料集 (確保日期欄位為字串或時間格式皆可比對)
df = pd.read_csv('business_dataset.csv')

# =====================================================================
# 步驟一：現況分析—了解當前獲利結構
# =====================================================================
print("\n【步驟一】進行品類一維排查（尋找公司的利潤頂頂樑柱與低於水平線者）")

# 以 category（品類）為單位，計算總營收與總利潤
category_pnl = df.groupby('category').agg({
    'revenue': 'sum',   # 每個品類的總營收
    'profit': 'sum'     # 每個品類的總利潤
}).reset_index()

# 計算「利潤偏離平均值」(用來看哪些品類高於/低於整體平均)
category_pnl['profit_change'] = (
    category_pnl['profit'] - category_pnl['profit'].mean()
)

# 格式化為「萬」元單位
category_pnl_show = pd.DataFrame()
category_pnl_show['品類'] = category_pnl['category']
category_pnl_show['總營收'] = (category_pnl['revenue'] / 10000).round(1).astype(str) + '萬'
category_pnl_show['總利潤'] = (category_pnl['profit'] / 10000).round(1).astype(str) + '萬'
category_pnl_show['利潤偏離平均值'] = (category_pnl['profit_change'] / 10000).round(1).astype(str) + '萬'

print(category_pnl_show.to_string(index=False))


# =====================================================================
# 步驟二：貢獻度歸因分析
# =====================================================================

# 切分時間：2025-07-01 之前（舊期）
prev = df[df['date'] < '2025-07-01'].groupby('category')['profit'].sum()

# 切分時間：2025-07-01（含）之後（新期）
curr = df[df['date'] >= '2025-07-01'].groupby('category')['profit'].sum()

# 計算各品類「利潤變動量」
delta = curr - prev

# 所有品類的總變動（整體利潤變化）
total_change = delta.sum()

# 計算各品類對「總變動的貢獻比例」
contribution = (delta / total_change) * 100
print(contribution)

# =====================================================================
#  步驟三：將步驟二的指標組裝成「變動與貢獻度拆解表」
# =====================================================================
# 將結果包裝成 DataFrame
contribution_df = pd.DataFrame({
    '舊期(H1)利潤': (prev / 10000).round(1).astype(str) + '萬',
    '新期(H2)利潤': (curr / 10000).round(1).astype(str) + '萬',
    '利潤變動量': (delta / 10000).round(1).astype(str) + '萬',
    '貢獻度': contribution.round(1).astype(str) + '%'
})

# 補上 Grand Total 列，讓統計大盤完全閉環
total_row = pd.DataFrame({
    '舊期(H1)利潤': [f"{round(prev.sum() / 10000, 1)}萬"],
    '新期(H2)利潤': [f"{round(curr.sum() / 10000, 1)}萬"],
    '利潤變動量': [f"{round(total_change / 10000, 1)}萬"],
    '貢獻度': ['100.0%']
}, index=['Grand Total'])

final_contribution_report = pd.concat([contribution_df, total_row])

print(final_contribution_report)
print(f"\n進入2025下半年後，全公司大盤利潤整整變動了 {round(total_change / 10000, 1)} 萬。")
