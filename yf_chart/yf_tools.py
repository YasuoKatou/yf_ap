import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import datetime
import pandas as pd
import yfinance as yf
import pandas as pd

_win_short = 13         # 移動平均(短)の日数
_win_long  = 25         # 移動平均(長)の日数
_history_period = '6mo' # 履歴データの取得期間
# 日本語フォントのパス
_font_path = "/system/fonts/NotoSansCJK-Regular.ttc"
# グラフ出力のパス
_graph_path="."

# 日本語フォントの設定
_jp_font = FontProperties(fname=_font_path)
plt.rcParams["axes.unicode_minus"] = False


def history(brand_code):
    # データ取得
    ticker = yf.Ticker(brand_code)
    return ticker.history(period=_history_period)

def avarage_short(df):
    # 移動平均を計算
    #return df['Close'].rolling(window=_win_short).mean()
    return df['Close'].rolling(window=_win_short).mean().shift(-(_win_short - 1))

def avarage_long(df):
    # 移動平均を計算
    #return df['Close'].rolling(window=_win_long).mean()
    return df['Close'].rolling(window=_win_long).mean().shift(-(_win_long - 1))

def adjust_row(df):
    # 各列の有効データ数
    min_count = df.count().min()

    print("最小データ数 =", min_count)

    # 先頭から最小数に揃える
    return df.iloc[:min_count]

def out_graph(df_plot, brand_code, brand_name, hinf=None):
    plt.figure(figsize=(12, 6))
    plt.plot(df_plot.index, df_plot["Close"], label='close')
    plt.plot(df_plot.index, df_plot["MA_short"], label=f'short({_win_short})')
    plt.plot(df_plot.index, df_plot["MA_long"], label=f'long({_win_long})')

    # 凡例の表示
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    #plt.show()

    # タイトルの追加
    t1 = f"{brand_name}({brand_code}) 株価チャート"
    now = datetime.datetime.now()
    if hinf is None:
        t2 = f'出力日時 {now.strftime('%y-%-m-%-d %H:%M')}'
    else:
        t2 = f'期間 {hinf['end'].strftime('%y-%-m-%-d')} 〜 {hinf['start'].strftime('%y-%-m-%-d')}'
    plt.title(f'{t1}\n{t2}', y=0.9, fontproperties=_jp_font)

    file_name = f"{_graph_path}/chart_{brand_code}.png"
    plt.savefig(file_name)
    print(f'グラフ保存完了: {file_name}')


if __name__ == '__main__':
    # 株価データの取得
    df = history('9508.T')
    # 移動平均の計算
    df['MA_short'] = avarage(df, _win_short)
    df['MA_long'] = avarage(df, _win_long) 
    # 日付を降順に並び替え
    df = df.sort_index(ascending=False)
    # データ数を最少に揃える
    df_plot = adjust_row(df)
    # グラフに出力
    out_graph(df_plot, '9508', '九州電力')

#[EOF]
