# -*- coding: utf-8 -*-

"""
5-2-3信心區間與不確定性
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

# 1. 設定繁體中文與負號支援
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# 2. 讀取資料集
df = pd.read_csv("comprehensive_market_stats.csv")


# =====================================================================
# 核心計算：手動推導 95% 信心區間（對齊文章內文的三個核心元素）
# =====================================================================
ci_results = []

for group_name, subset in df.groupby('AB測試分組'):
    # 元素 1：樣本量 (n) 與 樣本平均值 (Sample Mean)
    n = len(subset)
    sample_mean = subset['最終消費金額(元)'].mean()
    sample_std = subset['最終消費金額(元)'].std()
    
    # 核心統計量：標準誤差 (Standard Error, SE = s / sqrt(n))
    # 它代表「樣本平均值」的波動度
    standard_error = sample_std / np.sqrt(n)
    
    # 元素 3：信心水準 (Confidence Level = 95%)
    confidence_level = 0.95
    # 使用 t 分佈尋找臨界值（雙尾檢定，故兩側各留 2.5%）
    t_critical = stats.t.ppf((1 + confidence_level) / 2, df=n-1)
    
    # 元素 2：誤差界限 (Margin of Error, MOE)
    margin_of_error = t_critical * standard_error
    
    # 計算信賴區間的上下界
    ci_lower = sample_mean - margin_of_error
    ci_upper = sample_mean + margin_of_error
    
    ci_results.append({
        '組別': group_name,
        '樣本量(n)': n,
        '樣本平均值': round(sample_mean, 2),
        '標準差': round(sample_std, 2),
        '誤差界限(±)': round(margin_of_error, 2),
        '95%區間下界': round(ci_lower, 2),
        '95%區間上界': round(ci_upper, 2)
    })

# 轉換為 DataFrame 方便閱讀
df_ci = pd.DataFrame(ci_results)
print("\n【統計稽核：兩組 95% 信心區間報告】")
print(df_ci.to_string(index=False))

