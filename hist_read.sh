#
# $1 : 銘柄コード
# $2 : Tickerシンボルコード
#
no_hist() {
    echo "$tname not exist"
    # 履歴データを固定の期間(period)で取得し、DBに登録する
    python history2db.py \
        -sqlite_path $sqlite_path \
        -hist_period $hist_period \
        -brand_code  $brand_code  \
        -target_symbol $target_symbol
}
add_hist() {
    echo "$tname exist"
    # 履歴データを今日まで取得し、DBに登録する（from/to）
    #
    # ------------------------------
    # 取得開始日(from)を決定する
    # ------------------------------
    # 履歴の最後日を取得
    qry="select strftime('%Y%m%d',max(\"index\")) from $tname"
    #echo $qry
    dt=$(sqlite3 $db_opt_cmd $sqlite_path "$qry")
    # 履歴の最終日より７日前を開始日に設定する
    st_date=$(date --date "$dt 7 days ago" "+%Y-%m-%d")
    # ------------------------------
    # 取得終了日(from)を決定する
    # ------------------------------
    # 今日を取得終了日とする
    ed_date=$(date "+%Y-%m-%d")
    echo last date : $dt, start : $st_date, end : $ed_date
    # ------------------------------
    # 履歴データを期間(from/to)で取得し、DBに登録する
    # ------------------------------
    period="$st_date,$ed_date"
    python history2db.py \
        -sqlite_path $sqlite_path \
        -hist_period $period \
        -brand_code  $brand_code  \
        -target_symbol $target_symbol

}

source ./env.sh
brand_code=$1
target_symbol=$2
#echo symbol : $target_symbol
tname=hist_$brand_code
sqlite_path=./data/yfinance.db
# テーブルの存在チェック
qry="select count(1) from sqlite_master where type='table' and name='$tname'"
num=$(sqlite3 $db_opt_cmd $sqlite_path "$qry")
#echo count:$num
if [ "$num" -eq 1 ]; then
    add_hist
else
    no_hist
fi

#EOF
