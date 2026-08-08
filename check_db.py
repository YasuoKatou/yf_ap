import sqlite3
import pathlib

db_path_default = './data/yfinance.db.20260804'
tname01 = 'brand'       # 銘柄テーブル名
def check_01(db_path=db_path_default):
    '''
    sqlite dc のパスを確認する
    '''
    p = pathlib.Path(db_path)
    assert p.exists(), f'db not found ({db_path})'
    return db_path

def check_02(cur):
    '''
    銘柄テーブル(brand) の存在とレコード数の確認
    '''
    qry=f"select count(1) from sqlite_master where type='table' and name = '{tname01}'"
    cur.execute(qry)
    row = cur.fetchone()
    assert row[0] == 1, '{tname01} table not one'
    qry=f"select count(1) from {tname01}"
    cur.execute(qry)
    row = cur.fetchone()
    assert row[0] > 0, f'{tname01} is empty'
    print(f'{tname01} has {row[0]} records')

def get_brand_info(cur):
    qry = f"select brand_code, brand_name from {tname01} order by brand_code"
    cur.execute(qry)
    for row in cur:
        yield (row[0], row[1])

if __name__ == '__main__':
    db_path = check_01()
    print(f'db path : {db_path}')
    with sqlite3.connect(db_path) as conn:
        cur1 = conn.cursor()
        cur2 = conn.cursor()
        try:
            check_02(cur1)
            for brand in get_brand_info(cur1):
                print(f'{brand[0]}:{brand[1]}')
        finally:
            cur1.close()
            cur2.close()

#[EOF]
