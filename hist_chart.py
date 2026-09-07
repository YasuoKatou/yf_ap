import yf_chart.yf_tools as yft
import os
import sys
import sqlite3
import pandas as pd
from check_db import get_hist_info

sqlite_work = './data/yfinance.db.check'
val = os.getenv('sqlite_work')
if val:
    if val != sqlite_work:
        print(f'change db_path : {sqlite_work} to {val}')
        sqlite_work = val
else:
    print(f'db path : default [{sqlite_work}]')

def prepare_graph():
    # デフォルトのフォントパスの変更を確認
    change = False
    val = os.getenv('font_path')
    if val:
        if yft._font_path != val:
            print(f'font path : {yft._font_path} to {val}')
            yft._font_path = val
            change = True
    if not change:
        print(f'font path : default [{yft._font_path}]')

    # デフォルトの移動平均（短周期）の変更を確認
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

    # デフォルトの移動平均（長周期）の変更を確認
    change = False
    val = os.getenv('win_long')
    if val:
        val = int(val)
        if yft._win_long != val:
            print(f'ave long: {yft._win_long} to {val}')
            yft._win_long = val
            change = True
    if not change:
        print(f'ave long : default [{yft._win_long}]')

    # デフォルトのグラフ出力パスの変更を確認
    change = False
    val = os.getenv('graph_path')
    if val:
        if yft._graph_path != val:
            print(f'graph path : {yft._graph_path} to {val}')
            yft._graph_path = val
            change = True
    if not change:
        print(f'graph path : default [{yft._graph_path}]')

def make_graph(brand_code, brand_name, hist_data):
    df = hist_data[0]
    # 移動平均の計算
    df['MA_short'] = yft.avarage_short(df)
    df['MA_long' ] = yft.avarage_long(df)
    print(df)
    # 日付を降順に並び替え
    df = df.sort_index(ascending=False)
    # データ数を最少に揃える
    df_plot = yft.adjust_row(df)
    # グラフに出力
    #hist_data[1] = None
    yft.out_graph(df_plot, brand_code, brand_name, hist_data[1], hist_data[2])

def get_brand_info(cur, brand_code):
    cur.execute('select paypay from brand where brand_code = ?', (brand_code, ))
    return cur.fetchone()[0]

def readHistData(brand_code):
    qry = f'select * from hist_{brand_code} order by \"index\" desc limit 365'
    # データベースファイルに接続
    conn = sqlite3.connect(sqlite_work)

    try:
        # 全履歴データを取得
        df = pd.read_sql(qry, conn)
        df['index'] = pd.to_datetime(df['index'])
        df = df.set_index('index')
        # 履歴の情報を取得
        cur = conn.cursor()
        hinf = get_hist_info(cur, brand_code)
        paypay = get_brand_info(cur, brand_code)
        return [df, hinf, paypay]
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    brand_code = sys.argv[1] 
    brand_name = sys.argv[2]
    r = readHistData(brand_code)
    #print(r[0])
    #print(r[0].columns)
    #print(r[0r[0]index)
    prepare_graph()
    make_graph(brand_code, brand_name, r)

#[EOF]
