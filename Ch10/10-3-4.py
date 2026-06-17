"""
10-3-4 A/A測試概念引入—驗證實驗系統的零偏誤
"""


# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 載入原始資料
df = pd.read_pickle('cookie_cats_clean.pkl')

# 只取同一個版本（模擬 A/A）
df_aa = df[df["version"] == "gate_30"].copy()


def bootstrap_aa_test(data, n_iter=1000):
    diffs = []

    for _ in range(n_iter):
        sample = data.sample(frac=0.1, replace=True)

        split = len(sample) // 2
        group_A = sample.iloc[:split]
        group_B = sample.iloc[split:]

        rate_A = group_A["retention_7"].mean()
        rate_B = group_B["retention_7"].mean()

        diffs.append(rate_A - rate_B)

    return np.array(diffs)

diffs = bootstrap_aa_test(df_aa)

# 看 A/A 是否「以 0 為中心」
print("平均差異:", diffs.mean())
print("標準差:", diffs.std())
print("95% CI:", np.percentile(diffs, [2.5, 97.5]))


# 畫分布（很重要）
import matplotlib.pyplot as plt

plt.hist(diffs, bins=30)
plt.axvline(0, color="red", linestyle="--")
plt.title("A/A 測試: 留存率差異分布圖")
plt.show()


