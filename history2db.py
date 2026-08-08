import sqlite3
import yfinance as yf

'''
履歴データを取得し、DBに登録する
取引対象日のデータが存在しない場合、insert
対象日のデータが存在する場合、delete/insert を行う
'''

from ap_common import getArgs

# 起動パラメータの取得
args = getArgs({
    # 履歴情報を保存するDBのパス
    '-sqlite_path': {'type': str},
    # 履歴情報を取得する期間
    '-hist_period': {'type': str},
    # 履歴情報を取得する銘柄コード
    '-brand_code': {'type': str},
    # 履歴情報を取得するシンボルコード
    '-target_symbol': {'type': str},
})

def getHistory():
    print(f'get history (symbol:{args.target_symbol})')
    tc = yf.Ticker(args.target_symbol)
    if ',' in args.hist_period:
        dt = args.hist_period.split(',')
        return tc.history(start=dt[0], end=dt[1])
    else:
        return tc.history(period=args.hist_period)

def prepare(df):
    # indexの型を変換
    df.index = df.index.date
    # 日付を昇順に並び替え
    df = df.sort_index()
    return df

def getDataInfo(df):
    return {
        'start': df.index.min(),
        'end'  : df.index.max(),
        'count': len(df),
        'table_name': f'hist_{args.brand_code}',
    }

def appendHistTable(conn, df, table_name):
    df.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=True,
    )
    print(f'dataframe 2 {table_name}')

def delete4insert(cur, df_info):
    table_name = df_info['table_name']
    # select * from hist_AAPL where "index" between '2026-06-10' and '2026-06-19';
    start_date = df_info['start'].strftime('%Y-%m-%d')
    end_date   = df_info['end'  ].strftime('%Y-%m-%d')
    sql = f"delete from {table_name} where \"index\" between '{start_date}' and '{end_date}'"
    cur.execute(sql)
    #print(f'pass : {sql}')
    # 削除したレコード数を戻す
    cur.execute('SELECT changes()')
    del_recs = cur.fetchone()[0]
    print(f'delete table : {table_name} delete period : {start_date} - {end_date} recs ; {del_recs}')
    return del_recs

def getRecordCount(cur, table_name):
    sql = f'select count(1) from {table_name}'
    cur.execute(sql)
    row = cur.fetchone()
    return row[0]

def save2DB(df_info, df):
    with sqlite3.connect(args.sqlite_path) as conn:
        cur = conn.cursor()
        # テーブルの存在チェック
        table_name = df_info['table_name']
        sql = f"select name FROM sqlite_master WHERE name='{table_name}'"
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            # テーブルが存在する場合、重複するデータを削除する
            recs = getRecordCount(cur, table_name)
            print(f'{table_name} current records : {recs}')
            delete4insert(cur, df_info)
        # 取得したデータをDBに登録する
        appendHistTable(conn, df, table_name)

        recs = getRecordCount(cur, table_name)
        print(f'{table_name} records:{recs}')

        conn.commit()

if __name__ == '__main__':
    df = getHistory()
    # print(df.columns)
    df = prepare(df)
    df_info = getDataInfo(df)
    print(f'dataframe : {df_info}')
    save2DB(df_info, df)

#[EOF]
