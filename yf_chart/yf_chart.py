import argparse
import pathlib

import yf_tools as yft

parser = argparse.ArgumentParser(description='株価チャート作成')
parser.add_argument('--brand_list_file', help='銘柄一覧ファイルのパス', default='./brand_list.csv')
parser.add_argument('--ave_long_days' , help='移動平均(長)', default=25, type=int)
parser.add_argument('--ave_short_days', help='移動平均(短)', default=13, type=int)
parser.add_argument('--history_period', help='履歴データの取得期間', default='6mo')
parser.add_argument('--font_path'     , help='日本フォントのパス')
args = parser.parse_args()
fp1 = args.brand_list_file
p = pathlib.Path(fp1)
assert p.exists(), f'{fp1} not found'

yft._win_long       = args.ave_long_days
yft._win_short      = args.ave_short_days
yft._history_period = args.history_period
if args.font_path:
    yft._font_path  = args.font_path

def execute(brand_name, brand_code, brand_symbol):
    # 株価データの取得
    df = yft.history(brand_symbol)
    # 移動平均の計算
    df['MA_short'] = yft.avarage_short(df)
    df['MA_long' ] = yft.avarage_long(df)
    # 日付を降順に並び替え
    df = df.sort_index(ascending=False)
    # データ数を最少に揃える
    df_plot = yft.adjust_row(df)
    # グラフに出力
    yft.out_graph(df_plot, brand_code, brand_name)

header_line = True
with p.open(mode='r', encoding='utf8') as f:
    for line in f:
        #print(line, end='')
        if header_line:
            header_line = False
            continue
        work = line.split(',')
        if work[0] != '1':
            print(f'pass {work[3]} ({work[1]})')
            continue
        print(f'execute {work[3]} ({work[1]})')
        execute(work[3], work[1], work[2])

#[EOF]