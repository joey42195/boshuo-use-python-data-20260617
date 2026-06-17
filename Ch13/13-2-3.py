# -*- coding: utf-8 -*-
"""
13-2-3差分技術—把斜率拍扁
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller

# 1. 讀取 ts_sales.csv 數據並篩選咖啡機
df_sales = pd.read_csv("ts_sales.csv")
df_coffee = df_sales[df_sales['product'] == 'coffee_machine'].copy()
df_coffee['date'] = pd.to_datetime(df_coffee['date'])
df_coffee = df_coffee.sort_values('date')

#%%

# 2. 執行一階差分 (當期值 減 過去值)
# .diff() 預設就是計算一階差分 (periods=1)
df_coffee['units_diff'] = df_coffee['units'].diff()

# 3. 數據健康驗收：計算差分前後的標準差 (Standard Deviation)
std_original = df_coffee['units'].std()
std_diff = df_coffee['units_diff'].std()  # pandas 會自動忽略第一筆 NaN

print("=== 差分前後的波動度（標準差）檢驗 ===")
print(f"原始數據的標準差 (Std): {std_original:.2f}")
print(f"一階差分後的標準差 (Std): {std_diff:.2f}")

if std_diff < std_original:
    print("綠燈通告：差分後標準差顯著縮小！代表混亂的趨勢已收斂，數據正在變穩定。")
else:
    print("紅燈警告：差分後標準差反而變大，這可能存在過度差分的風險！")
print("-" * 45)

# 4. 執行科學驗收：差分後的 ADF 檢定
adf_result_diff = adfuller(df_coffee['units_diff'].dropna())
p_value_diff = adf_result_diff[1]
test_stat_diff = adf_result_diff[0]
print(f"檢定統計量 (Test Statistic): {test_stat_diff:.4f}")
print(f"關鍵 P-value 分數: {p_value_diff:.5f}\n\n")



print("=== 差分後的 ADF 科學檢定報告 ===")
print(f"一階差分後的 P-value: {p_value_diff:.5f}")
if p_value_diff < 0.05:
    print("綠燈通告：P-value < 0.05！成功拒絕虛無假設，數據正式轉為【平穩狀態】。")
else:
    print("紅燈警告：P-value 依舊大於 0.05，數據仍不平穩，請勿強行建模。")

#%%
# 補充：差分後的統計圖
import matplotlib.gridspec as gridspec

# =====================================================================
# 第一部分：繪製四宮格儀表板 (左上原始，其餘皆為差分後)
# =====================================================================
fig = plt.figure(figsize=(18, 11))
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 支援繁體中文
plt.rcParams['axes.unicode_minus'] = False              # 正常顯示負號

# 創建 2x2 網格
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.2)

# 定義促銷期區間（供視覺對照）
promo_start_date = df_coffee['date'].iloc[200]
promo_end_date = df_coffee['date'].iloc[240]

# --- 圖一 (左上)：原始銷量折線圖 ---
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(df_coffee['date'], df_coffee['units'], color='blue', alpha=0.7, marker='o', markersize=2, label='原始銷量 (Yt)')
ax1.axvspan(promo_start_date, promo_end_date, color='red', alpha=0.08, label='促銷區間')
ax1.set_title('原始銷售折線圖 (Original Series) - 均值隨時間飄移', fontsize=12, fontweight='bold')
ax1.set_ylabel('絕對銷量 (Units)', fontsize=11)
ax1.legend(loc='upper left')

# --- 圖二 (右上)：差分後的折線圖 ---
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(df_coffee['date'].iloc[1:], df_coffee['units_diff'].iloc[1:], color='crimson', alpha=0.8, marker='s', markersize=2, label='一階差分量 (ΔYt)')
ax2.axhline(y=0, color='black', linestyle='-', linewidth=1.2)
ax2.axvspan(promo_start_date, promo_end_date, color='red', alpha=0.08, label='促銷區間')
ax2.set_title('差分後折線圖 (First-order Difference) - 趨勢與高原已被拍扁', fontsize=12, fontweight='bold')
ax2.set_ylabel('銷量變動量 (ΔUnits)', fontsize=11)
ax2.legend(loc='upper left')

# 設定最大延遲階數 (Lag) 觀察 20 天
max_lags = 20

# --- 圖三 (左下)：差分數據 ACF 圖 ---
ax3 = fig.add_subplot(gs[1, 0])
# 記得 .dropna() 移除差分產生的第一個 NaN
plot_acf(df_coffee['units_diff'].dropna(), ax=ax3, lags=max_lags, title="③ 差分後 ACF - 慢性衰減消失，釋放每週週期規律")
ax3.set_ylim(-1.05, 1.05)
ax3.set_xlabel('延遲階數 (Lags / 天)', fontsize=11)
ax3.set_ylabel('自相關係數', fontsize=11)

# ---圖四 (右下)：差分數據 PACF 圖 ---
ax4 = fig.add_subplot(gs[1, 1])
plot_pacf(df_coffee['units_diff'].dropna(), ax=ax4, lags=max_lags, title="④ 差分後 PACF - 解放被趨勢綁架的直接因果 (準備定階)")
ax4.set_ylim(-1.05, 1.05)
ax4.set_xlabel('延遲階數 (Lags / 天)', fontsize=11)
ax4.set_ylabel('偏自相關係數', fontsize=11)

# 加上全圖大標題
plt.suptitle('時間序列前置診斷與術後驗收：從『原始非平穩』到『差分定態化』', fontsize=16, fontweight='bold', y=0.96)
plt.show()

# =====================================================================
#  第二部分：封裝並儲存至 Pickle，為下一階段建模預留伏筆
# =====================================================================
# 我們將清洗並處理好的咖啡機 DataFrame（包含原始銷量與差分銷量）封存
pickle_filename = "coffee_machine_ready.pkl"
df_coffee.to_pickle(pickle_filename)

print(f"=== 數據封存完畢 ===")
print(f"已成功將處理完成的資料儲存至：'{pickle_filename}'")
print(f"目前 DataFrame 欄位：{list(df_coffee.columns)}")




