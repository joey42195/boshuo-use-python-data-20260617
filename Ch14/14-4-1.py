# -*- coding: utf-8 -*-

"""
14-4-1競品流失追蹤—誰被擠出市場？
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
# 1. 量化替代效應的幅度 (Quantifying Cannibalization)
# 我們要計算「他牌_競品」在促銷期間的受創程度。這反映了兩項產品在消費者心中的替代強度。


# 1. 計算他牌競品的基準日均銷量 (第一月)
base_qty_C = df[(df['月份'] == '第一月(基準)') & (df['產品名稱'] == '他牌_競品')]['銷量'].mean()

# 2. 篩選促銷期間他牌競品的實際銷量
promo_data_C = df[(df['活動標籤'] == '大促期間') & (df['產品名稱'] == '他牌_競品')]
actual_qty_C = promo_data_C['銷量'].mean() # 促銷期間的日均

# 3. 計算銷量流失率 (Cannibalization Rate)
loss_rate_C = (actual_qty_C - base_qty_C) / base_qty_C
print(f"他牌_競品 促銷期間銷量變動：{loss_rate_C*100:.2f}%")


#%%

# 2. 區分「增量來源」：新需求 vs. 品牌轉換
# 這是分析師向決策層展示深度的時刻。我們必須拆解出銷量增長中，到底有多少是「有效增長」。
# 分析邏輯：
# 市場擴張 (Market Expansion)
# 品牌侵蝕 (Brand Switching)
# 數據觀測點：品類總量 (Category Volume)


# 計算促銷期間與基準期間，品類整體的日均總銷量
# 品類包含：主機 + 競品 (配件不計入，避免重複計算需求)

def get_cat_avg(label):
    temp = df[df['活動標籤'] == label]
    total_qty = temp[temp['產品名稱'].isin(['咖啡機_主機', '他牌_競品'])]['銷量'].sum()
    days = temp['日期'].nunique()
    return total_qty / days

base_cat_avg = get_cat_avg('常態營運')
promo_cat_avg = get_cat_avg('大促期間')

print(f"基準期品類日均總量：{base_cat_avg:.2f}")
print(f"促銷期品類日均總量：{promo_cat_avg:.2f}")
print(f"品類總量增長率：{((promo_cat_avg - base_cat_avg) / base_cat_avg)*100:.2f}%")



#%%

"""
市場總量檢驗整體計算
小數點計算可能因時間長度而有些許誤差
"""


import pandas as pd

# 載入資料
df = pd.read_pickle('sales_basic_14_1_2.pkl')

# ==============================================================================
# 1. 定義統一的日均銷量計算函式 (確保計算邏輯、天數分母完全一致)
# ==============================================================================
def get_daily_avg(activity_label, product_list):
    """
    計算特定活動期間內，指定產品組合的日均銷量
    """
    # 篩選活動標籤
    temp = df[df['活動標籤'] == activity_label]
    # 篩選產品品項
    temp = temp[temp['產品名稱'].isin(product_list)]
    
    total_qty = temp['銷量'].sum()
    days = temp['日期'].nunique()
    
    return total_qty / days if days > 0 else 0

# ==============================================================================
# 2. 設定表格結構與計算資料
# ==============================================================================
# 定義我們要產出表格的層級與對應的產品
target_structure = [
    {"層級": "品類總量", "指標": "主機+競品", "products": ['咖啡機_主機', '他牌_競品']},
    {"層級": "主機", "指標": "咖啡機_主機", "products": ['咖啡機_主機']},
    {"層級": "競品", "指標": "他牌_競品", "products": ['他牌_競品']}
]

summary_rows = []

# 循環計算每一列的數據
for row in target_structure:
    # 統一使用 '常態營運' 作為基準期，'大促期間' 作為促銷期
    base_avg = get_daily_avg('常態營運', row['products'])
    promo_avg = get_daily_avg('大促期間', row['products'])
    
    # 計算變動百分比
    if base_avg > 0:
        change_rate = ((promo_avg - base_avg) / base_avg) * 100
        change_str = f"{'+' if change_rate >= 0 else ''}{change_rate:.2f}%"
    else:
        change_str = "0.00%"
        
    # 儲存結果
    summary_rows.append({
        "層級": row["層級"],
        "指標": row["指標"],
        "基準期（日均）": round(base_avg, 2),
        "促銷期（日均）": round(promo_avg, 2),
        "變動": change_str
    })

# ==============================================================================
# 3. 轉換為 DataFrame 並輸出
# ==============================================================================
result_df = pd.DataFrame(summary_rows)

# 顯示結果
print(result_df.to_string(index=False))







