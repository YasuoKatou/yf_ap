import yf_chart.yf_tools as yft
import os
import sys
import sqlite3
import pandas as pd

sqlite_path = './data/yfinance.db'
val = os.getenv('sqlite_path')
if val:
    if val != sqlite_path:
        print(f'change db_path : {sqlite_path} to {val}')
        sqlite_path = val
else:
    print(f'db path : default [{sqlite_path}]')

def prepare_graph():
    change = False
    val = os.getenv('font_path')
    if val:
        if yft._font_path != val:
            print(f'font path : {yft._font_path} to {val}')
            yft._font_path = val
            change = True
    if not change:
        print(f'font path : default [{yft._font_path}]')

    change = False
    val = os.getenv('win_short')
    if val:
        val = int(val)
        if yft._win_short!= val:
            print(f'ave short: {yft._win_short} to {val}')
            yft._win_short = val
            change = True
    if not change:
        print(f'ave short : default [{yft._win_short}]')

    hchange = False
    val = os.getenv('win_long')
    if val:
        val = int(val)
        if yft._win_long != val:
            print(f'ave long: {yft._win_long} to {val}')
            yft._win_long = val
            change = True
    if not change:
        print(f'ave long : default [{yft._win_long}]')

    hchange = False
    val = os.getenv('graph_path')
    if val:
        if yft._graph_path != val:
            print(f'graph path : {yft._graph_path} to {val}')
            yft._graph_path = val
            change = True
    if not change:
        print(f'graph path : default [{yft._graph_path}]')

def make_graph(brand_code, brand_name, df):
    # 移動平均の計算
    df['MA_short'] = yft.avarage_short(df)
    df['MA_long' ] = yft.avarage_long(df)
    print(df)
    # 日付を降順に並び替え
    df = df.sort_index(ascending=False)
    # データ数を最少に揃える
    df_plot = yft.adjust_row(df)
    # グラフに出力
    yft.out_graph(df_plot, brand_code, brand_name)

def readHistData(brand_code):
    qry = f'select * from hist_{brand_code} order by \"index\" desc limit 365'
    # データベースファイルに接続
    conn = sqlite3.connect(sqlite_path)

    try:
        # 全履歴データを取得
        df = pd.read_sql(qry, conn)
        df['index'] = pd.to_datetime(df['index'])
        df = df.set_index('index')
        return df
    finally:
        conn.close()

if __name__ == '__main__':
    brand_code = sys.argv[1] 
    brand_name = sys.argv[2]
    df = readHistData(brand_code)
    #print(df)
    #print(df.columns)
    #print(df.index)
    prepare_graph()
    make_graph(brand_code, brand_name, df)

#[EOF]
