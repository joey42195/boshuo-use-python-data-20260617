# -*- coding: utf-8 -*-
"""
10-3-2分組均衡性檢查—樣本與SRM風險防線
"""
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 載入原始資料
df = pd.read_pickle('cookie_cats_clean.pkl')

# 檢查優化後的結果
print(df.info())

#%%

# 2. 分組均衡性檢查與 SRM 檢定 (9-2-3)
# 這是 A/B Testing 的「驗票」環節。如果分組不均，後面的統計數據再漂亮都是假的。
# 我們使用 卡方適合度檢定 (Chi-squared Goodness-of-Fit Test)。

from scipy.stats import chisquare

# --- 1. 樣本量對齊檢查 ---
actual_counts = df.groupby('version', observed=False).size()
print(f"實際分組人數:\n{actual_counts}")

# --- 2. SRM 樣本比例偏差檢定 ---
# 假設我們的實驗設定是 50:50 分流
total_users = actual_counts.sum()
expected_counts = [total_users / 2, total_users / 2]

# 執行卡方檢定
chi_stat, p_value = chisquare(actual_counts, f_exp=expected_counts)

print(f"\n卡方統計量: {chi_stat:.4f}")
print(f"SRM 檢定 p-value: {p_value:.4f}")

# 判斷結果
# 建議將 SRM 的警示門檻調嚴格一點，或是加上「偏差百分比」判斷
if p_value < 0.001:
    print("嚴重警報：SRM 偏差極大，必須停止分析。")
elif p_value < 0.05:
    deviation = abs(actual_counts['gate_30'] - actual_counts['gate_40']) / total_users * 100
    print(f"微弱警報：統計顯著但偏差率僅 {deviation:.2f}%。建議檢查分流器，但可謹慎繼續分析。")
else:
    print("數據通過均衡性檢查。")
    
    
    






