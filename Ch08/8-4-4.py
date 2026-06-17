
"""
8-4-4在OLAP中利用K-Means標籤進行多維下鑽

"""


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 載入算好的 K-Means 成果主檔
rfm_base = pd.read_csv('sales_kmeans.csv')
rfm_base.columns
df = pd.read_csv('customer_dataset.csv')
df.columns

# 日期轉換
df['date'] = pd.to_datetime(df['date'])

# 取年份
df['year'] = df['date'].dt.year


#%%

# merge 客群
df_merged = df.merge(
    rfm_base[['customer_id', 'Kmeans_seg']],
    on='customer_id',
    how='left'
)

df_merged['date'] = pd.to_datetime(df_merged['date'])
df_merged['year'] = df_merged['date'].dt.year

# 資料準備

df_merged = df.merge(
    rfm_base[['customer_id', 'Kmeans_seg']],
    on='customer_id',
    how='left'
)

# 年度總體變化（核心 KPI）

year_kpi = (
    df_merged.groupby('year')
    .agg(
        revenue=('revenue', 'sum'),
        customers=('customer_id', 'nunique')
    )
)

#%%
'''
第一層診斷（總體拆解）—營收變動從哪裡開始惡化？
'''

year_kpi['ARPU'] = year_kpi['revenue'] / year_kpi['customers']
year_kpi['revenue_change'] = year_kpi['revenue'].pct_change() * 100
year_kpi['customer_change'] = year_kpi['customers'].pct_change() * 100
year_kpi['arpu_change'] = year_kpi['ARPU'].pct_change() * 100

print(year_kpi.round(2))


print(year_kpi.loc[2025].round(2))

#%%

'''
第二層診斷—是哪一群客戶在拉低ARPU？
'''

# ---------------------------------------------------------------------
# 步驟 1：建立年度客群 KPI（基礎維度聚合）
# ---------------------------------------------------------------------
# 按年度與 K-Means 客群，統計總營收與不重複客戶數
segment_year = (
    df_merged.groupby(['year', 'Kmeans_seg'])
    .agg(
        revenue=('revenue', 'sum'),
        customers=('customer_id', 'nunique')
    )
    .reset_index()
)

# 動態計算各客群在該年度的 ARPU (總營收 / 總人數)
segment_year['ARPU'] = segment_year['revenue'] / segment_year['customers']

# ---------------------------------------------------------------------
# 步驟 2：轉成 RCA 樞紐透視化
# ---------------------------------------------------------------------
# 利用 pivot_table 將年度 (year) 展開至欄位，建立跨年度對照結構
# 建立跨年度對照之高維度樞紐透視表 (OLAP 多維資料集)
# index='Kmeans_seg'：以機器學習客群標籤作為列索引 (Row Index)
# columns='year'：將年度 (2024, 2025) 展開為欄位次維度 (Column Sub-index)
# values：同時計算三個核心指標。此時 columns 會形成「多層欄位索引 (MultiIndex Columns)」
seg_pivot = segment_year.pivot_table(
    index='Kmeans_seg',
    columns='year',
    values=['revenue', 'customers', 'ARPU']
)

# ---------------------------------------------------------------------
# 步驟 3：計算「變動量」（RCA 核心差值運算）
# ---------------------------------------------------------------------
# 建立一個獨立的 RCA 診斷DataFrame
# 直接繼承 seg_pivot 的客群標籤索引 (index)，確保資料列對齊完全一致
seg_change = pd.DataFrame(index=seg_pivot.index)

# 計算 2024 到 2025 年的指標淨變動量值（現況年 - 基準年）
# 跨年度指標淨變動量運算 (RCA 核心差值計算)
# 技術要點：由於 seg_pivot 具備多層索引，必須先指定指標名稱 ['ARPU']，再指定年度維度 [2025]
# 運算邏輯：現況年 (2025) - 基準年 (2024)，正值代表增長，負值代表衰退
seg_change['ARPU_change'] = seg_pivot['ARPU'][2025] - seg_pivot['ARPU'][2024]
seg_change['revenue_change'] = seg_pivot['revenue'][2025] - seg_pivot['revenue'][2024]
seg_change['customer_change'] = seg_pivot['customers'][2025] - seg_pivot['customers'][2024]

print("=" * 80)
print("步驟 3 輸出：依 ARPU 惡化程度排序之客群變動清單")
print("=" * 80)
print(seg_change.sort_values('ARPU_change'))

# ---------------------------------------------------------------------
# 步驟 4：找出「最大兇手」
# ---------------------------------------------------------------------
# 利用 idxmin() 自動捕捉 ARPU 負向變動最大的 Cluster 代號
worst_segment = seg_change['ARPU_change'].idxmin()
print("\n" + "=" * 80)
print(f"步驟 4 診斷報告：ARPU 最大拖累客群 ──> 【 {worst_segment} 】")
print("=" * 80)

# ---------------------------------------------------------------------
# 步驟 5：計算「貢獻度（Contribution %）」
# ---------------------------------------------------------------------
# 這是 RCA 的精華：計算該客群變動量佔整體總變動量的比例
# 將所有客群的 ARPU 變動量進行加總，求得總體大盤指標的淨變動絕對值
total_arpu_change = seg_change['ARPU_change'].sum()

# 計算各客群的損害/成長貢獻度 (Contribution %)
# 運算公式：(單一客群變動量 / 大盤總變動量) * 100
# 商業意義：精準衡量單一客群的變動對總體大盤指標造成了多少百分比的結構性影響
seg_change['contribution_%'] = (seg_change['ARPU_change'] / total_arpu_change * 100)

# 依據貢獻度進行排序，全面鎖定影響力結構
seg_change = seg_change.sort_values('contribution_%')

# ---------------------------------------------------------------------
# 步驟 6：輸出 RCA 表（最重要結果）
# ---------------------------------------------------------------------
print("\n" + "=" * 80)
print("步驟 6 終極成果：大數據根因分析 (RCA) 核心診斷大表")
print("=" * 80)
print(seg_change.round(2))
print("=" * 80)

#%%

'''
第三層診斷—為什麼「沉睡客」ARPU下降這麼多？
'''

# ---------------------------------------------------------------------
# 1、商品效應評估 (Segment ✕ Product)
# ---------------------------------------------------------------------
print("=" * 80)
print("診斷一：跨客群 ✕ 商品品類之總營收分佈 (橫向交叉表)")
print("=" * 80)

# 步驟 1：基礎資料聚合
# 按『客群標籤』與『商品品類』兩大維度加總營收，建立多維分析的底層基底
seg_product = df_merged.groupby(['Kmeans_seg', 'product'])['revenue'].sum().reset_index()

# 步驟 2：空間橫向對比 (橫向交叉表)
# 將 Kmeans_seg（客群）展至欄位，product（商品）保留在列索引，缺失值以 0 填補
# 商業意義：用以觀察不同客群在各大商品品類的總體營收貢獻基準
pivot_product = seg_product.pivot(
    index='product',
    columns='Kmeans_seg',
    values='revenue'
).fillna(0)
print(pivot_product.round(1))

print("\n" + "=" * 80)
print("診斷二：『沉睡客』逐年商品營收變動量拆解")
print("=" * 80)

# 步驟 3：引入時間維度 (跨年複合聚合)
# 按『年度』、『商品』與『客群』三維進行分組營收加總，用以捕捉跨年消長趨勢
product_year = df_merged.groupby(['year', 'product', 'Kmeans_seg'])['revenue'].sum().reset_index()

# 步驟 4：建立多層索引透視表
# 將年度（year）展開至欄位，商品與客群設定為雙層列索引 (MultiIndex)
pivot_prod_year = product_year.pivot_table(
    index=['product', 'Kmeans_seg'],
    columns='year',
    values='revenue',
    fill_value=0
)

# 步驟 5：計算跨年商品營收淨變動量值
# 現況年 (2025) - 基準年 (2024)，用以評估各品類在跨年度的失血程度（商品效應）
pivot_prod_year['change'] = pivot_prod_year[2025] - pivot_prod_year[2024]

# 【關鍵動作】利用 .xs() 切片函數，精準隔離出「沉睡客」的商品資料
# 指定關鍵字 '沉睡客'，並明確定義切片層級 level='Kmeans_seg'
# 資料工程意義：在不破壞結構的前提下，精準隔離出「沉睡客」在各大品類的跨年變動數據
sleeping_product_effect = pivot_prod_year.xs('沉睡客', level='Kmeans_seg')
print(sleeping_product_effect.sort_values('change').round(1))

# 步驟 6：自動化根因捕捉
# 利用 .idxmin() 函數自動找出變動量欄位（change）中負值最大（即衰退最嚴重）的商品列索引名稱
worst_product = sleeping_product_effect['change'].idxmin()
print(f"\n產品層面診斷結論：『沉睡客』營收重災區商品 ──> 【 {worst_product} 】")


# ---------------------------------------------------------------------
# 2、通路效應評估 (Segment ✕ Channel)
# ---------------------------------------------------------------------
print("\n" + "=" * 80)
print(" 診斷三：『沉睡客』行銷觸達通路之年度效益衰退拆解")
print("=" * 80)

# 步驟 7：行銷渠道多維聚合
# 轉換下鑽視角，按『年度』、『客群』與『行銷通路』三維進行營收加總
seg_channel = df_merged.groupby(['year', 'Kmeans_seg', 'channel'])['revenue'].sum().reset_index()


# 步驟 8：建立通路結構透視表
# 列索引採用雙層結構（通路 ✕ 客群），欄位依年度展開，用以對照各接觸管道的演變
pivot_channel = seg_channel.pivot_table(
    index=['channel', 'Kmeans_seg'],
    columns='year',
    values='revenue',
    fill_value=0
)

# 步驟 9：計算通路跨年變動量
# 計算各管道在 2024 到 2025 年間引流變現能力的淨變動絕對值（通路效應）
pivot_channel['change'] = pivot_channel[2025] - pivot_channel[2024]

# 【關鍵動作】再次利用 .xs() 切片，精準鎖定「沉睡客」在各通路的反饋
# 從「通路 ✕ 客群」的雙層索引中，精準隔離出僅屬於「沉睡客」的通路數據看板
sleeping_channel_effect = pivot_channel.xs('沉睡客', level='Kmeans_seg')
print(sleeping_channel_effect.sort_values('change').round(1))

# 步驟 10：自動化渠道黑洞捕捉
# 利用 .idxmin() 自動擷取 change 欄位中衰退最劇烈的通路名稱，作為戰略調整依據
worst_channel = sleeping_channel_effect['change'].idxmin()
print(f"\n通路層面診斷結論：『沉睡客』效益惡化最嚴重通路 ──> 【 {worst_channel} 】")
print("=" * 80)

#%%
