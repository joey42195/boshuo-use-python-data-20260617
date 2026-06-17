# -*- coding: utf-8 -*-

"""
5-1-2標準差與業務穩定性
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 設定繪圖風格與中文顯示
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 載入全功能統計資料集
df = pd.read_csv("comprehensive_market_stats.csv")

# =====================================================================
# 商務情境工程：將 12,730 筆訂單，依照「藍色廣告版位」隨機模擬聚合成 168 個小時的「每小時出貨包裏數」
# =====================================================================
np.random.seed(42)
# 篩選出引導出巨大流量的 Layout_Blue 訂單
blue_orders = df[df['廣告版位設計'] == 'Layout_Blue']

# 將這些訂單隨機分配到 168 個小時中 (模擬一整週 7天 x 24小時 的電商大促庫存需求)
hours = np.random.randint(0, 168, size=len(blue_orders))
hourly_summary = pd.DataFrame({'小時': hours, '訂單': 1})
hourly_packages = hourly_summary.groupby('小時').sum()['訂單'].reindex(range(168), fill_value=0)

# 計算核心統計量：平均值 (μ) 與 標準差 (σ)
mu = hourly_packages.mean()
sigma = hourly_packages.std()

# =====================================================================
# 運算：雙邊判定 (Mean ± 2σ) 與 單邊判定 (Mean + 1.65σ)
# =====================================================================
lower_2sigma = mu - 2 * sigma
upper_2sigma = mu + 2 * sigma
safety_capacity_95 = mu + 1.65 * sigma

print("=" * 70)
print("5-1-2 標準差商務風控核心指標計算報告")
print("=" * 70)
print(f"每小時平均包裏處理需求 (Mean): {mu:.1f} 件")
print(f"每小時出貨量隨機波動標準差 (Sigma): {sigma:.1f} 件")
print("-" * 70)
print(f"[雙邊風控] 物流中心黃金營運排班區間 (Mean ± 2σ):")
print(f"範圍: [{lower_2sigma:.1f}] 到 [{upper_2sigma:.1f}] 件包裏/小時")
print(f"商業意義: 落在這區間內皆屬正常隨機波動，低於叫『閒置浪費』，高於叫『爆倉風險』。")
print("-" * 70)
print(f"[單邊風控] 95% 承諾防斷貨 ── 每小時最低安全發貨容量容量基準 (Mean + 1.65σ):")
print(f"基準線: {safety_capacity_95:.1f} 件包裏/小時")
print(f" 商業意義: 只要我們向物流商租用此容量，將有 95% 的大促時間絕對不會發生斷流塞車！")
print("=" * 70 + "\n")

# =====================================================================
# 視覺化：繪製大促期間每小時波動圖，並動態畫上雙邊與單邊的控盤防線
# =====================================================================
plt.figure(figsize=(15, 6))
plt.plot(hourly_packages.index, hourly_packages.values, label='每小時真實包裏量', color='#1f77b4', alpha=0.8, linewidth=2)

# 畫上平均線
plt.axhline(mu, color='black', linestyle='-', linewidth=2, label=f'常態期望值 (Mean): {mu:.1f}')

# 畫上雙邊判定 Mean ± 2σ (紅色區間)
plt.axhline(upper_2sigma, color='red', linestyle='--', linewidth=1.5, label=f'雙邊上限 (Mean + 2σ): {upper_2sigma:.1f}')
plt.axhline(lower_2sigma, color='red', linestyle='--', linewidth=1.5, label=f'雙邊下限 (Mean - 2σ): {lower_2sigma:.1f}')
plt.fill_between(hourly_packages.index, lower_2sigma, upper_2sigma, color='red', alpha=0.08, label='95% 正常波動黃金區間')

# 畫上單邊判定 Mean + 1.65σ (紫色防線)
plt.axhline(safety_capacity_95, color='purple', linestyle=':', linewidth=2.5, label=f'單邊 95% 安全容量防線 (Mean + 1.65σ): {safety_capacity_95:.1f}')

plt.title('5-1-2 標準差實戰：利用時序波動數據構建企業「雙邊風控牆」與「單邊安全容量」', fontsize=16, fontweight='bold')
plt.xlabel('大促營運時間 (第 1 小時 至 第 168 小時)', fontsize=12)
plt.ylabel('每小時包裏吞吐量 (件)', fontsize=12)
plt.xlim(0, 168)
plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', fontsize=10)
plt.tight_layout()

plt.show()