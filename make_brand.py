from datetime import date
import pandas as pd
import sqlite3

from ap_common import getArgs

# 起動パラメータの取得
args = getArgs({
    # 銘柄情報が登録されたExcelファイルのパス
    '-excel_path': {'type': str},
    # 銘柄情報を保存するDBのパス
    '-sqlite_path': {'type': str},
    # 銘柄情報を登録するテーブル名
    '-table_name': {'type': str},
})
# Excel読込み
print(f'read excel file : {args.excel_path}')
df = pd.read_excel(args.excel_path)

# 列名を英語に変更
#print('[before]')
#print(df.columns)
col_names_us = {
        '日付': 'data_date', 'コード': 'brand_code',
        '銘柄名': 'brand_name',
        '市場・商品区分': 'market',
        '33業種コード': 'ind33_code',
        '33業種区分': 'ind33_name',
        '17業種コード': 'ind17_code',
        '17業種区分': 'ind17_name',
        '規模コード': 'scale_code',
        '規模区分': 'scale_name',
}
df = df.rename(columns=col_names_us)
#print('[after]')
#print(df.columns)

print(df.dtypes)
# 列の型を定義
col_data_type = {
        #'data_date': int,
        'brand_code': str,
        'brand_name': str,
        'market': str,
        'ind33_code': str,
        'ind33_name': str,
        'ind17_code': str,
        'ind17_name': str,
        'scale_code': str,
        'scale_name': str,
}
# 列の型を変換
for col_name, col_type in col_data_type.items():
    df[col_name] = df[col_name].astype(col_type)
    df[col_name] = df[col_name].replace('-', None)
#print('[after]')
#print(df.columns)

# Tickerシンボル列の追加
df['ticker_symbol'] = df['brand_code'] + '.T'

# SQLite接続
print(f'save to sqlite : {args.sqlite_path}.{args.table_name}')
conn = sqlite3.connect(args.sqlite_path)

# テーブル作成＆データ登録
df.to_sql(
    args.table_name,
    conn,
    if_exists="replace",
    index=False,
#    dtype=col_data_type,
)

conn.close()

print("登録完了")

#[EOF]
