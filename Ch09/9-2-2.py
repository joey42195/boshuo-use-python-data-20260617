# -*- coding: utf-8 -*-

"""
9-2-2實作多維漏斗矩陣
"""
import pandas as pd
import numpy as np
# 載入資料
df = pd.read_csv('funnel.csv')
df.columns


def generate_dimensional_funnel(df, dimension):
    """
    動態根據傳入的維度（Dimension），計算各子群體的步驟轉換率與去重人數
    """
    # 1. 依據維度與事件進行分組統計去重人數
    grouped = df.groupby([dimension, 'event'])['user_id'].nunique().unstack()
    
    # 2. 確保標準電商漏斗的順序
    stages = ['view_item', 'add_to_cart', 'begin_checkout', 'purchase']
    # 預防資料中漏掉特定事件，僅選取存在的欄位
    available_stages = [s for s in stages if s in grouped.columns]
    grouped = grouped[available_stages]
    
    # 3. 計算步驟轉換率 (Step Conversion Rate)
    funnel_matrix = pd.DataFrame(index=grouped.index)
    
    # 基礎用戶數
    funnel_matrix['基礎流量(View)'] = grouped['view_item']
    
    # 計算各階段步驟轉換率
    if 'add_to_cart' in grouped.columns:
        funnel_matrix['瀏覽 ──> 加購 (CR)'] = (grouped['add_to_cart'] / grouped['view_item']).map('{:.2%}'.format)
    if 'begin_checkout' in grouped.columns:
        funnel_matrix['加購 ──> 結帳 (CR)'] = (grouped['begin_checkout'] / grouped['add_to_cart']).map('{:.2%}'.format)
    if 'purchase' in grouped.columns:
        funnel_matrix['結帳 ──> 購買 (CR)'] = (grouped['purchase'] / grouped['begin_checkout']).map('{:.2%}'.format)
        
    return funnel_matrix

# ---- 實戰應用：對「裝置(device)」維度進行下鑽分析 ----
print("【維度下鑽：裝置維度 (Device) 漏斗矩陣】")
device_funnel = generate_dimensional_funnel(df, 'device')
print(device_funnel.to_string())