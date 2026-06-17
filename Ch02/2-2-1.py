# -*- coding: utf-8 -*-

"""
2-2-1缺失值檢查與分布觀察
"""

import seaborn as sns
import pandas as pd

# 1. 載入內建的鐵達尼號資料集
df = sns.load_dataset('titanic')

# ---------------------------------------------------------------------
# 第一步：檢查各欄位的「絕對缺失數」與「相對百分比」
# ---------------------------------------------------------------------
print("第一步 全站欄位缺失率總覽：")

# 計算每個欄位的缺失值（NaN）數量，isnull() 會將缺失值標記為 True
null_counts = df.isnull().sum() # sum() 會把 True 視為 1 進行加總

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

