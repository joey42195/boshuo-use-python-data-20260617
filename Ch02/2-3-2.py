
# -*- coding: utf-8 -*-
"""
2-3-2離群值處理方法
"""

import pandas as pd
import numpy as np

# 1. 載入資料
df = pd.read_csv('E-commerce_Dirty_Dataset.csv')

# 強制將關鍵欄位轉換為數值型態（排除 NaN 影響）
df['conversion_rate'] = pd.to_numeric(df['conversion_rate'], errors='coerce')
df['spending'] = pd.to_numeric(df['spending'], errors='coerce')


# ---------------------------------------------------------------------
# 策略一：直接移除 (Remove) ➔ 適用於明確的錯誤資料
# ---------------------------------------------------------------------
print("\n策略一：直接移除 清理突破界限的轉換率地雷")

# 現實世界的合理邊界：轉換率不可能大於 100% (1.0)
df_removed = df[df['conversion_rate'] <= 1.0]

print(f"   - 處理前全站總筆數: {len(df)} 筆")
print(f"   - 剃除 >100% 轉換率地雷後筆數: {len(df_removed)} 筆")
print(f"   ➔ 成功移除 {len(df) - len(df_removed)} 筆不合理的系統污染數據！")


# ---------------------------------------------------------------------
# ✂️ 策略二：雙向截斷處理 (Clip / Winsorize) ➔ 用 .clip() 處理消費金額
# ---------------------------------------------------------------------
print("\n" + "-" * 80)
print("策略二：雙向截斷 對消費金額 (spending) 使用「1% 至 99% 截斷處理」")
print("-" * 80)

# 商業邏輯：設定上下界
# 使用 1% 與 99% 分位數建立上下界
lower_value = (
    df['spending']
    .quantile(0.01)
)

upper_value = (
    df['spending']
    .quantile(0.99)
)

print(f"   - 統計防線劃定：")
print(f"     底層 1% 地平線 (Lower bound) : {lower_value:.2f} 元")
print(f"     頂層 99% 天際線 (Upper bound): {upper_value:.2f} 元")

# 複製一份資料進行截斷
df_clipped = df.copy()


# 使用 clip() 限制極端值範圍
df_clipped['spending_clipped'] = (
    df_clipped['spending']
    .clip(
        lower=lower_value,
        upper=upper_value
    )
)


print(f"\n   -[前後對照：")
print(f"     截斷前 ➔ 最小值: {df_clipped['spending'].min():.2f} 元 | 最大值: {df_clipped['spending'].max():.2f} 元")
print(f"     截斷後 ➔ 最小值: {df_clipped['spending_clipped'].min():.2f} 元 | 最大值: {df_clipped['spending_clipped'].max():.2f} 元")



# ---------------------------------------------------------------------
# 策略三：對數轉換 (Log Transformation) ➔ 長尾分布
# ---------------------------------------------------------------------
print("\n" + "-" * 80)
print("策略三：對數轉換 使用 np.log1p() 處理長尾資料")
print("-" * 70)

# 對右偏極其嚴重的 spending 進行對數轉換（使用 log1p 確保遇到 0 值時不會出錯）
df_log = df.copy()
df_log['spending_log'] = np.log1p(df_log['spending'])

# 對照偏態（Skewness）：越接近 0 代表越符合穩定的常態分布
print(f"   - 原始 spending 的偏態值 : {df_log['spending'].skew():.4f} (極度右偏長尾)")
print(f"   - 轉換後 spending_log 偏態值: {df_log['spending_log'].skew():.4f} (完美回歸穩定)")


# 建立副本避免污染原始資料
df_log = df.copy()

# 先檢查不合法值（log1p 無法處理 <= -1）
invalid_count = (
    df_log['spending'] <= -1
).sum()

print(f"   - 無法進行 log1p() 的資料筆數: {invalid_count} 筆")

# 建立合法條件
valid_condition = df_log['spending'] > -1

# 先建立空欄位
df_log['spending_log'] = np.nan

# 僅對合法值進行 log1p()
df_log.loc[valid_condition, 'spending_log'] = np.log1p(
    df_log.loc[valid_condition, 'spending']
)

# 對照偏態（Skewness）：越接近 0 代表越符合穩定的常態分布
print(f"   - 原始 spending 的偏態值 : {df_log['spending'].skew():.4f} (極度右偏長尾)")
print(f"   - 轉換後 spending_log 偏態值: {df_log['spending_log'].skew():.4f} (完美回歸穩定)")



