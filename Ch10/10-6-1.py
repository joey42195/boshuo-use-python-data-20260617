# -*- coding: utf-8 -*-

"""
10-6-1風險量化
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False


# 載入原始資料
df = pd.read_pickle('cookie_cats_clean.pkl')
df.columns


# 1. 準備數據：從 DataFrame 提取數值
# 分別篩選出 gate_30 與 gate_40 的數據
group_30 = df[df['version'] == 'gate_30']['retention_7']
group_40 = df[df['version'] == 'gate_40']['retention_7']

# 提取參數：成功次數 (Sum) 與 總人數 (Count)
a_success = group_30.sum()
a_total = group_30.count()

b_success = group_40.sum()
b_total = group_40.count()

print(f"Gate 30 (A): 留存 {a_success}, 總數 {a_total}")
print(f"Gate 40 (B): 留存 {b_success}, 總數 {b_total}")

# A 組 (gate_30): 留存人數 19023, 總人數 44700 (約 42.56%)
# B 組 (gate_40): 留存人數 18206, 總人數 45489 (約 40.02%)

# 2. 執行蒙地卡羅模擬
n_samples = 100000
# 這裡使用弱先驗 Beta(1, 1)
samples_A = np.random.beta(a_success + 1, a_total - a_success + 1, size=n_samples)
samples_B = np.random.beta(b_success + 1, b_total - b_success + 1, size=n_samples)

# 3. 計算核心指標：勝率 (Prob Better) 與 提升率 (Uplift)
prob_B_better = (samples_B > samples_A).mean()
print(f"Gate 40 優於 Gate 30 的機率: {prob_B_better:.4f}")

# 計算相對提升率：(B - A) / A
uplift_samples = (samples_B - samples_A) / samples_A

# 計算 95% 的信賴區間（第 2.5 百分位數到第 97.5 百分位數）
ci_lower = np.percentile(uplift_samples, 2.5)
ci_upper = np.percentile(uplift_samples, 97.5)

print(f"平均相對提升率: {uplift_samples.mean():.2%}")
print(f"95% 信賴區間: [{ci_lower:.2%}, {ci_upper:.2%}]")


#%%
"""
10-6-1風險量化
"""
# 接續之前的 samples_A, samples_B
# 計算 A 贏過 B 的差值
loss_A_minus_B = np.maximum(samples_A - samples_B, 0)

# 計算預期損失 (Expected Loss)
# 如果我們選擇 B 組，平均會損失多少留存率？
expected_loss_B = loss_A_minus_B.mean()

print(f"如果選擇 Gate 40，預計會損失的留存率絕對值: {expected_loss_B:.4%}")
print(f"相對衰退率: {(samples_B.mean() - samples_A.mean()) / samples_A.mean():.2%}")

#%%





