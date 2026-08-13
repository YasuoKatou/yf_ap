import datetime
import sqlite3
import pathlib

from ap_common import count_business_days

db_path_default = './data/yfinance.db.check'
tname01 = 'brand'       # 銘柄テーブル名
tname02_pfx = 'hist_'   # 履歴テーブル接頭句
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

def check_03(cur, tno, brand_code, brand_name):
    print(f'{tno:5} {brand_code}:{brand_name}')
    qry = f"select count(1),min(\"index\"), max(\"index\") from {tname02_pfx}{brand_code}"
    try:
        cur.execute(qry)
        row = cur.fetchone()
        recs = row[0]
        dt1  = row[1]
        dt2  = row[2]
        #print(type(dt2))
        dt1o  = datetime.datetime.strptime(dt1, "%Y-%m-%d")
        dt2o  = datetime.datetime.strptime(dt2, "%Y-%m-%d")
        today = datetime.date.today()
        pdays = count_business_days(dt2o.date(), today)
        ldays = count_business_days(dt1o.date(), dt2o.date())
        print(f'      pass {pdays} days {dt2} - {dt1}, {recs} days lost {ldays-recs} days')
        return [pdays]
    except sqlite3.OperationalError as ex:
        print(f'error : {ex}')
        return None
    except Exception as ex:
        assert False, (f'unexpected error\n{ex}')

if __name__ == '__main__':
    db_path = check_01()
    print(f'db path : {db_path}')
    pmax = 0
    pmin = 365 * 100
    plist = {}
    with sqlite3.connect(db_path) as conn:
        cur1 = conn.cursor()
        cur2 = conn.cursor()
        try:
            check_02(cur1)
            tno = 0
            for brand in get_brand_info(cur1):
                tno += 1
                r = check_03(cur2, tno, brand[0], brand[1])
                if r is None:
                    continue
                if r[0] < pmin:
                    pmin = r[0]
                if pmax < r[0]:
                    pmax = r[0]
                if r[0] in plist:
                    plist[r[0]] += 1
                else:
                    plist[r[0]] = 1
        finally:
            cur1.close()
            cur2.close()
    print(f'pass : {pmin} - {pmax} days')
    #print(plist)
    ##sorted_d = dict(sorted(plist.items()))
    wk = sorted(plist.items(), key=lambda x:x[0])

    for k, v in wk:
        print(f'\t{k:4} : {v:5}')

#[EOF]
