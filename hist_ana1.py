import sqlite3

import pandas as pd

import yf_chart.yf_tools as yft

sqlite_work = './data/yfinance.db.check'

_ana1_cols = ['Close', 'MA_short', 'MA_long']
_elements = 10
_hist_tname1 = 'hist_ana1'

def drop_hist_ana1_table(conn):
    cur = conn.cursor()
    cur.execute(f'drop table if exists {_hist_tname1}')
    cur.close()
    print(f'drop table {_hist_tname1}')


def calc1(conn, table_name):
    '''
    履歴データの直近(10営業日分)の終値を取得する
    '''
    #print(table_name)
    qry = f'select "index", "Close" from {table_name} order by \"index\" desc limit 50'
    df = pd.read_sql(qry, conn)
    if len(df) < 50:
        print(f'\n{table_name} data not enough ({len(df)})')
        return None
    df['index'] = pd.to_datetime(df['index'])
    df = df.set_index('index')
    #print(f'date : {df.index[0]}')
    last_date = df.index[0]
    df['MA_short'] = yft.avarage_short(df)
    df['MA_long' ] = yft.avarage_long(df)

    # GC date
    gc_date = None
    for idx in range(0, df.count().min()):
        if df.at[df.index[idx], 'MA_short'] < df.at[df.index[idx], 'MA_long']:
            if 0 < idx:
                gc_date = df.index.tolist()[idx-1]
            break
        if 30 < idx:
            # within 30 days
            break

    # 先頭10行を取得して転置
    df2 = df[_ana1_cols].head(_elements).T

    # 列名を変更
    df2.columns = [f"a{i}" for i in range(1, _elements+1)]

    df3 = pd.DataFrame([df2.to_numpy().ravel()])
    cols = []
    for col in _ana1_cols:
        cols += [f"{col}{i}" for i in range(1, _elements+1)]
    df3.columns = (cols)
    df3['last_date'] = last_date
    df3['gc_date']   = gc_date

    return df3

def ana1():
    qry="select name from sqlite_master where type='table' and name like 'hist%' order by name"
    t_num = 0
    with sqlite3.connect(sqlite_work) as conn:
        drop_hist_ana1_table(conn)
        cur = conn.cursor()
        cur.execute(qry)
        for row in cur:
            tname = row[0]
            rec = calc1(conn, tname)
            #print(rec)
            if rec is None:
                continue
            rec.insert(0, 'table_name', [tname])
            #print(rec)
            #break
            t_num += 1
            # テーブルに保存
            rec.to_sql(
                _hist_tname1,
                conn,
                if_exists="append",
            )
            print(f'\r({t_num})insert into {_hist_tname1} value {tname}', end='')
            if t_num >= 10:
                # 後工程のため、途中で中断する
                #break
                pass
            #print(f'ana1 : {tname}')
        cur.close()
    print('\nfinished ...')

if __name__ == '__main__':
    ana1()

#[EOF]
