# -*- coding: utf-8 -*-

"""
13-2-2 觀察平穩性
3、科學檢定(ADF Test)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 設定字體以顯示中文 (根據作業系統可能需調整)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 1. 數據讀取與排序
df = pd.read_csv('ts_sales.csv', parse_dates=['date'])
df_coffee = df[df['product'] == 'coffee_machine'].copy()
df_coffee['date'] = pd.to_datetime(df_coffee['date'])
df_coffee = df_coffee.sort_values('date')

#%%

from statsmodels.tsa.stattools import adfuller

series_original = df_coffee['units']

# --- 證據三：執行科學裁判 ADF 檢定 ---
adf_result = adfuller(series_original)
p_value = adf_result[1]
test_stat = adf_result[0]

# 將檢定結果文字化，直接寫在右側畫布上

report_text = (
    f"=== 【證據三：ADF 科學檢定報告】 ===\n\n"
    f"1. 虛無假設 (H0)：序列不平穩 (存在單位根)\n"
    f"2. 對立假設 (H1)：序列已達到平穩\n\n"
    f"檢定統計量 (Test Statistic): {test_stat:.4f}\n"
    f"關鍵 P-value 分數: {p_value:.5f}\n\n"
    f"-----------------------------------------\n"
    f"最終判決：\n"
)

if p_value >= 0.05:
    report_text += (
        f"P-value ({p_value:.3f}) >= 0.05，無法拒絕 H0！\n"
        f"科學證據確鑿：此數據【確定為非平穩 (Non-stationary)】。\n"
        f"理由：7-8 月促銷導致均值嚴重飄移，系統存在長期記憶毒素。\n\n"
        f"下一步行動建議：\n"
        f"請立刻放棄直接建模！數據必須移交下一節進行『一階差分處理』。"
    )
else:
    report_text += f" P-value < 0.05，拒絕 H0。數據平穩，可直接建模。"

print(report_text)


