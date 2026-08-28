import datetime
import sqlite3
import unicodedata
from bs4 import BeautifulSoup
from email import message_from_bytes

from ap_common import get_env_db

'''
import requests
def read_html(url):
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    return BeautifulSoup(res.text, 'html.parser')
'''

def read_mhtml_file(html_path):
    # MHTMLファイルの読込み
    with open(html_path, 'rb') as f:
        msg = message_from_bytes(f.read())

    # HTMLパートの抽出
    html_content = None
    if msg.is_multipart():
        #print('multipart')
        for part in msg.walk():
            if part.get_content_type() == 'text/html':
                html_content = part.get_payload(decode=True).decode(
                    part.get_content_charset() or 'utf-8', errors='ignore'
                )
                break
    else:
        #print('single part')
        if msg.get_content_type() == 'text/html':
            html_content = msg.get_payload(decode=True).decode(
                msg.get_content_charset() or 'utf-8', errors='ignore'
            )

    assert html_content, 'not found html contents'
    #print(html_content)
    return BeautifulSoup(html_content, 'html.parser')

def read_mhtml(source_url):
    #soup = read_html(source_url)
    soup = read_mhtml_file(source_url)
    print(soup.title.string)
    #elms = soup.select('div.brand-list__container')
    #elms = soup.select('div')
    #elms = soup.find_all('div', class_='page-content')
    elms = soup.find_all('div', class_='brand-list__container')
    #print(len(elms))
    brands = []
    for brand_elm in elms:
        #print(type(brand_elm))
        # codenumber
        div_code = brand_elm.find('div', class_='codenumber')
        div_name = brand_elm.find('div', class_='brand')
        #print(f'[{div_code.text}] {div_name.text}')
        brands.append([div_code.text, div_name.text])
    return brands

def jp_brand(source_url):
    brands = read_mhtml(source_url)
    print(f'paypay jp : {len(brands)}')
    return brands

def us_brand(source_url):
    brands = read_mhtml(source_url)
    print(f'paypay us : {len(brands)}')
    return brands

def add_paypay_column(cur):
    # 列を追加するテーブルの存在確認
    table_name = 'brand'
    cur.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table' and name=?",
        (table_name,)
    )
    assert cur.fetchone()[0], f'[{table_name}] table not found ...'
    # 対象テーブルに追加する列が存在するかを確認
    cur.execute(f'PRAGMA table_info({table_name})')
    columns = cur.fetchall()
    column_names = [col[1] for col in columns]
    column_name = 'paypay'
    if column_name in column_names:
        cur.execute(f'update {table_name} set {column_name} = ?', (None, ))
        print(f'clear {column_name} to {table_name}')
    else:
        cur.execute(f'ALTER TABLE {table_name} ADD COLUMN {column_name} TEXT')
        print(f'add {column_name} to {table_name}')

def set_paypay(cur, brand):
    qry1 = 'select brand_name from brand where brand_code = ?'
    qry2 = 'update brand set paypay = ? where brand_code = ?'
    qry3 = 'insert into brand (data_date, brand_code, brand_name, ticker_symbol, paypay) values (?, ?, ?, ?, ?)'
    paypay_symbol = 'P'
    now = datetime.datetime.now()
    data_date = int(now.strftime('%Y%m%d'))
    for country, brand_info in brand.items():
        upd_count = 0
        ins_count = 0
        for item in brand_info:
            cur.execute(qry1, (item[0], ))
            row = cur.fetchone()
            if row is None:
                ticker_symbol = f'{item[0]}.T' if country == 'jp' else item[0]
                cur.execute(qry3, (data_date, item[0], item[1], ticker_symbol, paypay_symbol, ))
                print(f'INFO append brand [{item[0]}] ({item[1]})')
                ins_count += 0
                continue
            name = unicodedata.normalize('NFKC', row[0])
            name1 = name.replace('＆', '&').replace(' ', '')
            name2 = item[1].replace('＆', '&').replace(' ', '')
            if name1 != name2:
                print(f'WARN [{item[0]}] name diff [{name}] v.s. [{item[1]}]')
            cur.execute(qry2, (paypay_symbol, item[0], ))
            upd_count += 1
        print(f'brand update : {upd_count}, insert : {ins_count}')


if __name__ == '__main__':
    brand = {}
    # 日本株
    #url = 'https://www.paypay-sec.co.jp/stock/list/'
    url = './data/paypay_jp.mhtml'
    brand['jp'] = jp_brand(url)
    # 米国株
    #url = 'https://www.paypay-sec.co.jp/us-stock/list/'
    url = './data/paypay_us.mhtml'
    brand['us'] = us_brand(url)

    db_path = get_env_db()
    assert db_path, 'db file path not found ...'
    print(f'db path : {db_path}')
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        try:
            add_paypay_column(cur)
            set_paypay(cur, brand)
            conn.commit()
        finally:
            cur.close()

#[EOF]
