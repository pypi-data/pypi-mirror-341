import os
import pandas as pd
import numpy as np
from src.utils.molecular_weights import MOLECULAR_WEIGHTS

def create_ascii_plot(data, column, width=80, height=20, title=None):
    """
    創建 ASCII 圖表用於終端機顯示
    
    Parameters:
    data (pd.DataFrame): 要繪製的數據
    column (str): 要繪製的列名
    width (int): 圖表的寬度（字符）
    height (int): 圖表的高度（字符）
    title (str): 圖表標題
    
    Returns:
    str: ASCII 圖表
    """
    if data.empty or column not in data.columns:
        return f"沒有 {column} 的數據可用"
    
    # 提取時間和值
    times = data['Time'].values
    values = data[column].values
    
    # 計算最小和最大值
    min_time, max_time = min(times), max(times)
    min_val, max_val = min(values), max(values)
    
    # 為值範圍添加一些邊距
    value_range = max_val - min_val
    if value_range == 0:  # 處理常數值
        value_range = abs(max_val) * 0.1 or 1.0
        min_val = max_val - value_range
    else:
        margin = value_range * 0.1
        min_val -= margin
        max_val += margin
    
    # 創建空的圖表畫布
    plot = [[' ' for _ in range(width)] for _ in range(height)]
    
    # 繪製坐標軸
    for y in range(height):
        plot[y][0] = '│'
    for x in range(width):
        plot[height-1][x] = '─'
    plot[height-1][0] = '└'
    
    # 繪製數據點
    prev_x, prev_y = None, None
    for i, (t, v) in enumerate(zip(times, values)):
        # 將數據點轉換為圖表坐標
        x = int((t - min_time) / (max_time - min_time) * (width - 2)) + 1
        y = height - 1 - int((v - min_val) / (max_val - min_val) * (height - 2)) - 1
        
        # 確保坐標在範圍內
        x = max(1, min(width-1, x))
        y = max(0, min(height-2, y))
        
        # 繪製點
        plot[y][x] = '*'
        
        # 用線連接點
        if prev_x is not None and prev_y is not None:
            if abs(x - prev_x) > 1 or abs(y - prev_y) > 1:
                # 使用 Bresenham 的線算法連接點
                dx = abs(x - prev_x)
                dy = abs(y - prev_y)
                sx = 1 if prev_x < x else -1
                sy = 1 if prev_y < y else -1
                err = dx - dy
                
                cx, cy = prev_x, prev_y
                while cx != x or cy != y:
                    e2 = 2 * err
                    if e2 > -dy:
                        err -= dy
                        cx += sx
                    if e2 < dx:
                        err += dx
                        cy += sy
                    
                    # 在繪製前檢查邊界
                    if 0 <= cy < height and 0 <= cx < width:
                        if plot[cy][cx] == ' ':
                            plot[cy][cx] = '·'
        
        prev_x, prev_y = x, y
    
    # 將圖表轉換為字符串
    plot_str = ''
    if title:
        # 居中標題
        title_padding = max(0, (width - len(title)) // 2)
        plot_str += ' ' * title_padding + title + '\n'
    
    # 添加 y 軸標籤
    header = f"│ {column} ({min_val:.2f} 到 {max_val:.2f})" + ' ' * (width - 15) + '\n'
    plot_str += header
    
    for row in plot:
        plot_str += ''.join(row) + '\n'
    
    # 添加 x 軸標籤
    footer = f"時間 ({min_time:.1f} 到 {max_time:.1f})"
    footer_padding = max(0, (width - len(footer)) // 2)
    plot_str += ' ' * footer_padding + footer + '\n'
    
    return plot_str

def print_ascii_summary(result_df, species_list):
    """
    打印物種濃度趨勢的 ASCII 摘要
    
    Parameters:
    result_df (pd.DataFrame): 結果數據框
    species_list (list): 要顯示的物種名稱列表
    """
    if result_df.empty:
        print("沒有可顯示的數據")
        return
    
    # 打印摘要標題
    print("\n" + "="*80)
    print("濃度趨勢摘要 (ASCII 圖表)")
    print("="*80)
    
    # 為每個物種創建 ASCII 圖表
    for species in species_list:
        # 確定正確的列名
        if f'{species} (%)' in result_df.columns:
            col = f'{species} (%)' 
            title = f"{species} 濃度 (%)"
        elif f'{species} (ppm)' in result_df.columns:
            col = f'{species} (ppm)'
            title = f"{species} 濃度 (ppm)"
        else:
            print(f"警告: 未找到 {species} 的數據")
            continue
        
        # 創建並打印 ASCII 圖表
        plot = create_ascii_plot(result_df, col, width=80, height=15, title=title)
        print("\n" + plot)
        print("-"*80)
        
        # 打印統計數據
        first_val = result_df[col].iloc[0]
        last_val = result_df[col].iloc[-1]
        min_val = result_df[col].min()
        max_val = result_df[col].max()
        avg_val = result_df[col].mean()
        
        print(f"{species} 的統計數據:")
        print(f"  起始值: {first_val:.2f}")
        print(f"  最終值: {last_val:.2f}")
        print(f"  變化: {last_val - first_val:.2f} ({((last_val - first_val) / first_val * 100) if first_val != 0 else 0:.2f}%)")
        print(f"  最小值: {min_val:.2f}")
        print(f"  最大值: {max_val:.2f}")
        print(f"  平均值: {avg_val:.2f}")
        print("="*80)

def print_simple_trend_table(result_df, species_list, num_points=10):
    """
    打印簡單的趨勢表，顯示固定間隔的濃度值
    
    Parameters:
    result_df (pd.DataFrame): 結果數據框
    species_list (list): 要顯示的物種名稱列表
    num_points (int): 表中要顯示的點數
    """
    if result_df.empty:
        print("沒有可顯示的數據")
        return
    
    # 獲取每個物種的列名
    columns = []
    headers = []
    
    for species in species_list:
        if f'{species} (%)' in result_df.columns:
            columns.append(f'{species} (%)')
            headers.append(f'{species}(%)')
        elif f'{species} (ppm)' in result_df.columns:
            columns.append(f'{species} (ppm)')
            headers.append(f'{species}(ppm)')
    
    if not columns:
        print("未找到請求的物種的匹配列")
        return
    
    # 選擇固定間隔的行
    if len(result_df) <= num_points:
        selected_rows = result_df
    else:
        indices = [int(i * (len(result_df) - 1) / (num_points - 1)) for i in range(num_points)]
        selected_rows = result_df.iloc[indices]
    
    # 打印表頭
    print("\n" + "="*80)
    print("物種濃度趨勢表")
    print("="*80)
    
    # 構建標題行
    header_row = f"{'時間':>10}"
    for h in headers:
        header_row += f" | {h:>10}"
    print(header_row)
    print("-"*len(header_row))
    
    # 打印數據行
    for _, row in selected_rows.iterrows():
        data_row = f"{row['Time']:>10.1f}"
        for col in columns:
            data_row += f" | {row[col]:>10.2f}"
        print(data_row)
    
    print("="*80)

def print_terminal_visualizations(result_df):
    """
    打印終端機友好的可視化
    
    Parameters:
    result_df (pd.DataFrame): 結果數據框
    """
    # 定義要顯示的物種
    main_species = ['O2', 'CO2', 'NOx', 'NH3']
    
    # 打印 ASCII 圖表
    print_ascii_summary(result_df, main_species)
    
    # 打印簡單趨勢表
    print_simple_trend_table(result_df, main_species, num_points=15)
    
    # 打印最終值
    final_values = result_df.iloc[-1].copy()
    print("\n" + "="*60)
    print("最終濃度值 (最後時間步)")
    print("="*60)
    
    # 打印時間
    print(f"時間: {final_values['Time']} s")
    print("-"*60)
    
    for species in main_species:
        if f'{species} (%)' in result_df.columns:
            print(f"{species}: {final_values[f'{species} (%)']:>8.2f} %")
        elif f'{species} (ppm)' in result_df.columns:
            print(f"{species}: {final_values[f'{species} (ppm)']:>8.2f} ppm")
    
    print("="*60)
    
    # 返回最終結果字符串
    result_str = f"""============================================================
FINAL CONCENTRATION VALUES (LAST TIMESTEP)
============================================================
Time: {final_values['Time']} s
------------------------------------------------------------
DRY-BASE MOLE FRACTIONS:
   O2: {final_values['O2 (%)']:>8.2f} %
   N2: {final_values['N2 (%)']:>8.2f} %
  CO2: {final_values['CO2 (%)']:>8.2f} %
CO: {final_values['CO (%)']*10000:>8.2f} ppm
------------------------------------------------------------
Temperature: {final_values['Temperature (K)']:>8.2f} K
------------------------------------------------------------
NOx: {final_values['NOx (ppm)']:>8.2f} ppm
NH3: {final_values['NH3 (ppm)']:>8.2f} ppm

============================================================
"""
    return result_str 