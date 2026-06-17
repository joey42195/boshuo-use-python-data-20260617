# -*- coding: utf-8 -*-

"""
6-2-1環比—短期策略的溫度計
"""

import pandas as pd

# =====================================================================
# 6-2-1 環比（MoM / DoD）— 短期策略的溫度計實作
# =====================================================================

# 1. 載入時間序列資料集
df = pd.read_csv("Store_Item_Demand_2025.csv")

# 2. 確保日期格式，並聚合為「全站每日總營運銷量」
df['date'] = pd.to_datetime(df['date'])
daily_market = df.groupby('date')['sales'].sum().reset_index()

# 3. 核心技術：利用 pct_change(1) 一鍵計算與「前一期（昨日）」相比的日環比變動率
# 備註：1 代表平移一格。若是月資料，算出來的就是月環比 (MoM)；此處為日資料，即為日環比 (DoD)。
daily_market['日環比變動率'] = daily_market['sales'].pct_change(1)

# 4. 轉換為百分比格式 (例如：0.0532 -> 5.3%)，方便直覺閱讀
daily_market['日環比(%)'] = (daily_market['日環比變動率'] * 100).round(1)

# 查看計算結果
print("【全站每日銷量與環比診斷報告】")
print(daily_market.head(5).to_string(index=False))

#%%


import pandas as pd

# =====================================================================
# 6-2-1 月環比（MoM）— 中長期營運的指南針實作
# =====================================================================

# 1. 載入時間序列資料集
df = pd.read_csv("Store_Item_Demand_2025.csv")
df['date'] = pd.to_datetime(df['date'])

# 2. 核心技術：重採樣（Resample）與月環比計算
# Step A: 將 'date' 設為索引（Resample 的必要前提）
df_indexed = df.set_index('date')

# Step B: 使用 .resample('ME') 將數據按「月底(Month End)」聚合，並計算每月的總銷量
# 備註：在較新版的 Pandas 中，'M' 已更名為 'ME' (Month End)
monthly_market = (
    df_indexed['sales']
    .resample('ME')    # 或是 resample('M')
    .sum()
    .reset_index()
)

# Step C: 利用 pct_change(1) 計算與「前一期（上個月）」相比的月環比變動率
monthly_market['月環比變動率'] = (
    monthly_market['sales']
    .pct_change(1)
)

#  3.轉換為百分比格式，並擷取美麗的月份名稱
monthly_market['月份'] = monthly_market['date'].dt.strftime('%Y-%m')
monthly_market['月環比(%)'] = (monthly_market['月環比變動率'] * 100).round(1)

# 4. 重新排版欄位，讓業務報告更乾淨
monthly_report = monthly_market[['月份', 'sales','月環比變動率',  '月環比(%)']].rename(columns={'sales': '當月總銷量'}).reset_index()

print("【全站月度銷量與環比診斷報告】")
print(monthly_report.to_string(index=False))

