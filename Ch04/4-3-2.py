# -*- coding: utf-8 -*-

"""
4-3-2 Z-score標準化
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# 設定繁體中文與負號支援
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# 1. 讀取資料集
df = pd.read_csv('eCommerceUser.csv')

# 2. 使用 sklearn 特徵工程模組進行轉換
# (A) 對 income 與 spending 進行 Min-Max 正規化 (映射至 0~1)
mm_scaler = MinMaxScaler()
df[['income_mm', 'spending_mm']] = mm_scaler.fit_transform(df[['income', 'spending']])
print(df[['income_mm', 'spending_mm']])

# (B) 對 spending 進行 Z-score 標準化 (轉為標準差單位)
zs_scaler = StandardScaler()
df['spending_z'] = zs_scaler.fit_transform(df[['spending']])
print(df['spending_z'])

# 3. 初始化 1 列 2 行橫向大畫布
fig, axes = plt.subplots(1, 2, figsize=(16, 7.5), facecolor='white')


# =====================================================================
# 左圖 (A): 4-3-1 Min-Max 正規化 ➔ 觀察「收入與消費的同步步調」
# =====================================================================
# 為了避免 5128 筆資料在折線圖上擠成黑洞，我們抽樣前 50 筆用戶來清晰觀察相對關係
df_sample = df.head(50).copy().reset_index()

axes[0].plot(df_sample.index, df_sample['income_mm'], color='#005088', linewidth=2, marker='o', label='年收入 (Min-Max 化)')
axes[0].plot(df_sample.index, df_sample['spending_mm'], color='#e67e22', linewidth=2, linestyle='--', marker='s', label='消費金額 (Min-Max 化)')

axes[0].set_title("圖 A：Min-Max 正規化應用 (前 50 筆用戶對照)\n核心任務：消除數萬元與數十萬的尺度鴻溝，觀察「誰變高、誰下降」", 
                 fontsize=12, weight='bold', color='#005088', pad=15)
axes[0].set_xlabel("用戶抽樣流水號 (Sample Index)", fontsize=11)
axes[0].set_ylabel("映射後相對數值 (0 ~ 1 區間)", fontsize=11)
axes[0].grid(True, linestyle=':', alpha=0.5)
axes[0].legend(fontsize=10, loc='upper right')

# =====================================================================
# 右圖 (B): 4-3-2 Z-score 標準化 ➔ 獵殺大盤中的「離群值」
# =====================================================================
# 繪製全體 5128 筆用戶消費金額的 Z-score 分布密度
sns.kdeplot(data=df, x='spending_z', ax=axes[1], fill=True, color='#11caa0', alpha=0.15, linewidth=2.5)
# 用地毯圖 (rugplot) 在底部打上實體數據點，可看到右側那 20 筆極端離群值
sns.rugplot(data=df, x='spending_z', ax=axes[1], color='#e74c3c', height=0.06, alpha=0.6)

# 繪製相對位置防線：Z = 0 (全體平均線), Z = +3 (極端異常防線)
axes[1].axvline(0, color='#2c3e50', linestyle='-', linewidth=1.5, label='大盤消費平均值 (Z = 0)')
axes[1].axvline(3, color='#e74c3c', linestyle=':', linewidth=2, label='高達三個標準差防線 (Z = +3)')

# 幫讀者高亮標示出右側被程式刻意放大的超級大戶區
axes[1].axvspan(3, df['spending_z'].max() + 0.5, color='#e74c3c', alpha=0.1)
axes[1].text(3.5, 0.15, "離群值獵殺區\n這群 VIP 被生成器\n刻意放大了 3~8 倍！", color='#c0392b', fontsize=10, weight='bold')

axes[1].set_title("圖 B：Z-score 標準化應用 (全量 5128 筆異常診斷)\n核心任務：脫離原始金額單位，轉化為「距離大盤平均幾個標準差」", 
                 fontsize=12, weight='bold', color='#11caa0', pad=15)
axes[1].set_xlabel("消費金額 Z-score 轉換值 (單位：標準差 $\sigma$)", fontsize=11)
axes[1].set_ylabel("分布密度 (Density)", fontsize=11)
axes[1].grid(True, linestyle=':', alpha=0.5)
axes[1].legend(fontsize=10, loc='upper right')

# 4. 頂部大標題絕對定位
fig.text(0.5, 0.95, "章節 4-3 數據尺度轉換：Min-Max 步調共振 vs Z-score 異常獵殺實戰", 
         ha='center', fontsize=16, fontweight='bold', color='#2c3e50')

plt.tight_layout()
plt.subplots_adjust(top=0.86)

plt.show()

# 核心單行代碼：計算 Z-score 並篩選出超越 3 個標準差的極端長尾高價值用戶
print(df[((df['spending'] - df['spending'].mean()) / df['spending'].std()) > 3])