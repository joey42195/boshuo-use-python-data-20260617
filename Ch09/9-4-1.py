# -*- coding: utf-8 -*-
"""
9-4-1行為流向還原—從漏斗事件到流失原因建模
"""

import pandas as pd
import plotly.graph_objects as go

# ==========================================
# 1. 讀取現有的漏斗行為日誌資料（funnel.csv）
# ==========================================
df_logs = pd.read_csv('funnel.csv')

# 確保時間欄位格式正確，並依據使用者與時間軸嚴格排序
df_logs['timestamp'] = pd.to_datetime(df_logs['timestamp'])


# 建立時間序列行為資料，首先讀取使用者行為日誌，並依時間排序：
df_logs = df_logs.sort_values(['user_id', 'timestamp']).reset_index(drop=True)

# ==========================================
# 2. 資料工程：利用位移函數（Shift）找出用戶的「下一步行為」
# ==========================================

# 利用 groupby 鎖定同一個工作階段，並將 event 向上位移一格，取得下一步
df_logs['next_event'] = df_logs.groupby('session_id')['event'].shift(-1)

# 鎖定目標：篩選出在「手機端（mobile）」且觸發了「開始結帳（begin_checkout）」的紀錄
df_target = df_logs[
    (df_logs['device'] == 'mobile') & 
    (df_logs['event'] == 'begin_checkout')
].copy()


# ==========================================
# 3. 商業邏輯對齊：將量化斷點對應至質化 RCA 去向
# ==========================================

def map_to_sankey_destination(row):
    # 狀況 A：成功推進漏斗
    if row['next_event'] == 'purchase':
        return '2. 完成購買 (漏斗下一步)'
    
    # 狀況 B：用戶卡關流失，我們依據特徵歸納出 4 大核心質化去向（確保節點不重複）
    else:
        if row['inventory_status'] == 'out_of_stock':
            return '4. 走向客服/常見問題 (卡關諮詢)' # 合併點 A
        
        elif row['discount_rate'] >= 0.40:
            return '3. 返回商品詳情頁 (確認規格/比價)'
        
        else:
            if row['shipping_cost'] > 20:
                return '4. 走向客服/常見問題 (卡關諮詢)' # 合併點 B（兩者在圖上會合流）
            elif row['delivery_days'] >= 5:
                return '5. 跳回首頁 (尋找替代商品)'
            else:
                return '6. 直接離開網站 (體驗挫折放棄)'

# 應用映射函數，衍生出桑基圖的終點欄位
df_target['sankey_destination'] = df_target.apply(map_to_sankey_destination, axis=1)

# ==========================================
# 4. 數據聚合：計算各個分流管道的用戶數（Value）
# ==========================================
df_sankey_counts = (
    df_target
    .groupby('sankey_destination')
    .size()
    .reset_index(name='user_count')
)

print(df_sankey_counts)

# ==========================================
# 5. 餵入 Plotly 繪製動態桑基圖
# ==========================================
print("\n正在產生動態互動式桑基圖...")

# 定義視覺節點名稱（0 代表源頭，1~5 代表五個流向）
nodes = ["1. 開始結帳（Mobile）"] + list(df_sankey_counts['sankey_destination'])

# 建立 Plotly 要求的結構
sources = [0] * len(df_sankey_counts)            # 源頭全部固定為 index 0
targets = list(range(1, len(nodes)))             # 目標對應 nodes 的後續位置
values = list(df_sankey_counts['user_count'])    # 流量大小

fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 18,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = nodes,
      # 視覺色彩規劃：源頭藍、成功綠、質化診斷黃/橘、流失紅
      color = ["#2b5c8f", "#48C9B0", "#F4D03F", "#EB984E", "#A6ACAF", "#EC7063"]
    ),
    link = dict(
      source = sources,
      target = targets,
      value = values,
      color = "rgba(170, 170, 170, 0.35)" # 優雅的半透明流向灰
  ))])

# 完美避坑：使用正確的 title_font_size 參數
fig.update_layout(
    title_text=f"漏斗下鑽診斷：Mobile 端結帳流失用戶之質化行為路徑 (總樣本數: {sum(values)} 人)",
    title_font_size=16
)

# 儲存與網頁呈現
fig.write_html("9-4-1_sankey_from_csv.html")
fig.show()
print("成功！請至專案目錄查看 '9-4-1_sankey_from_csv.html' 互動式網頁圖表。")