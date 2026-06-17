# -*- coding: utf-8 -*-
"""
10-4-3機率模擬實作—使用蒙地卡羅方法進行貝氏A/B比較
"""
import pandas as pd
import numpy as np


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
print(uplift_samples)

# 計算 95% 的信賴區間（第 2.5 百分位數到第 97.5 百分位數）
ci_lower = np.percentile(uplift_samples, 2.5)
ci_upper = np.percentile(uplift_samples, 97.5)

print(f"平均相對提升率: {uplift_samples.mean():.2%}")
print(f"95% 信賴區間: [{ci_lower:.2%}, {ci_upper:.2%}]")



