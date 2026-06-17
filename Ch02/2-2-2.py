# -*- coding: utf-8 -*-

"""
2-2-2缺失值的本質分類
"""

import seaborn as sns
import pandas as pd

# 1. 載入內建的鐵達尼號資料集
df = sns.load_dataset('titanic')

# ---------------------------------------------------------------------
# 第一步：檢查各欄位的「絕對缺失數」與「相對百分比」
# ---------------------------------------------------------------------
print("第一步 全站欄位缺失率總覽：")

# 計算每個欄位的缺失值（NaN）數量
# isnull() 會將缺失值標記為 True
# sum() 會把 True 視為 1 進行加總
null_counts = df.isnull().sum()

# 計算每個欄位的缺失比例（百分比）
# mean() 會計算 True 的平均值，也就是缺失值比例
# 乘以 100 轉換為百分比
# round(2) 表示四捨五入到小數點第 2 位
null_ratios = (df.isnull().mean() * 100).round(2)

# 建立缺失結構表，只顯示有缺件的欄位
df_missing = pd.DataFrame({'缺失絕對值 (筆)': null_counts, '缺失百分比 (%)': null_ratios})
print(df_missing[df_missing['缺失絕對值 (筆)'] > 0])
print(f"\n資料總計 {len(df)} 筆，發現 age、embarked 等欄位存在破洞，")
print(f"      而 deck (船艙等級) 的缺失率竟然高達驚人的 {null_ratios['deck']}%！")


# ---------------------------------------------------------------------
# 第二步：結構拆解 ➔ 缺失值是否是隨機發生的？
# ---------------------------------------------------------------------
print("\n" + "-" * 70)
print("第二步 ：觀察 deck (船艙等級) 缺失值在不同船票階級 (pclass) 的分布")
print("-" * 70)

# 建立一個新欄位，標記該乘客的船艙資訊是否「遺失」
df['is_deck_missing'] = df['deck'].isnull()

# 交叉矩陣：計算不同社會階級 (pclass: 1=頭等艙, 3=三等艙) 的船艙缺失率
class_missing_matrix = (
    df.groupby('pclass')['is_deck_missing']
      .agg(['count', 'sum', 'mean'])
)

# 修改欄位名稱
class_missing_matrix.columns = [
    '總乘客人數',
    '船艙缺失人數',
    '該階層缺失率 (%)'
]

# 轉換成百分比
class_missing_matrix['該階層缺失率 (%)'] = (
    class_missing_matrix['該階層缺失率 (%)'] * 100
).round(2)

print(class_missing_matrix)
print("\n發現...缺失值根本不是隨機出現的！")
print("   - 頭等艙 (pclass 1) 的船艙缺失率只有 22.69%")
print("   - 三等艙 (pclass 3) 的底層貧民，船艙缺失率竟然高達 97.56%！幾乎全滅！")