# -*- coding: utf-8 -*-

"""
14-1-2數據初步檢查
"""


# 實戰範例：數據初步檢查清單


# 1. 載入數據與結構檢視
# 首先確認資料是否正確載入，並檢查欄位型態是否符合預期。


import pandas as pd

# 載入資料 (確保使用 utf-8-sig 以處理中文亂碼問題)
df = pd.read_csv('sales_basic.csv', encoding='utf-8-sig')

# 查看資料前 5 筆與欄位資訊
print(df.head())
print(df.info())

# 檢查要點：
# 日期 欄位是否為 datetime 型態？（若非，需轉換）。
# 營收 與 利潤 是否有空值 (NaN)？

# 將「日期」欄位從字串(object) 轉換為 時間型態(datetime)
df['日期'] = pd.to_datetime(df['日期'])

# 再次檢查型態
print(df['日期'].dtype) 
# 輸出應為：datetime64[ns]


#%%

# 2. 商務邏輯一致性檢查
# 針對我們設計的「兩月對比」模型，需確認基準月與促銷月的樣本數是否對等。

# 檢查各月份的資料列數
month_counts = df.groupby('月份').size()
print(f"各月紀錄筆數：\n{month_counts}")

# 檢查各產品的平均單價，確認促銷是否有如期發生
price_check = df.groupby(['產品名稱', '活動標籤'])['單價'].mean()
print(f"\n單價檢查：\n{price_check}")

# 洞察：
# 在 咖啡機_主機 的 大促期間，單價應該剛好是 4000（原價 5000 的 8 折）。
# 若出現 4500 這種數值，分析師應立即追蹤血緣：是系統設定錯誤，還是部分客戶沒有套用到折扣？


#%%

# 3. 利潤異常與極端值偵測
# 促銷期間最怕出現「負毛利」而不自知，或是異常的大單歪曲了增量計算。

# 檢查是否有負利潤的情況
negative_profit = df[df['利潤'] < 0]
if not negative_profit.empty:
    print(f"發現利潤異常紀錄：\n{negative_profit}")
else:
    print("數據檢查：無負利潤紀錄。")

# 檢查銷量分布 (是否有極端值)
print(df.groupby('產品名稱')['銷量'].describe())

#%%

# 為了能更直觀地感受這份資料的結構，可以畫出基礎的銷量走勢圖：
# 這張圖能幫助你快速確認：
# 第一月（基準月）是否平穩。
# 促銷期（第二月）是否有明顯的銷量噴發。

# 實戰：繪製全品類銷量趨勢圖
# 我們使用 Python 的 Seaborn 套件來繪製這張 60 天的走勢圖。
# 這張圖表將清晰地劃分出第一月的「常態」與第二月的「變動」。


import matplotlib.pyplot as plt
import seaborn as sns

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 建立圖表畫布
plt.figure(figsize=(15, 7))

# 繪製折線圖：按日期與產品名稱繪製銷量走勢
sns.lineplot(data=df, x='日期', y='銷量', hue='產品名稱', marker='o')

# 標註促銷區間 (第 41 天到 47 天)
plt.axvspan(df['日期'].iloc[120], df['日期'].iloc[141], color='red', alpha=0.1, label='大促期間')

# 加入基準線參考 (第一月主機平均銷量)
baseline_A = df[(df['月份'] == '第一月(基準)') & (df['產品名稱'] == '咖啡機_主機')]['銷量'].mean()
plt.axhline(y=baseline_A, color='gray', linestyle='--', alpha=0.6, label='主機基準線')

# 圖表美化
plt.title('60 天全產品銷量走勢圖：基準月 vs. 促銷月', fontsize=16)
plt.xlabel('日期', fontsize=12)
plt.ylabel('銷量 (Qty)', fontsize=12)
plt.legend(loc='upper left')
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

#%%

df.to_pickle('sales_basic_14_1_2.pkl')








