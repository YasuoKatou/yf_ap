#!/bin/bash
source ./env.sh
# 起動引数の日付とログの日付が一致する銘柄の履歴データを更新する
# ログのフォーマット
#   hist_3787|1.174|2026-08-20 00:00:00
log_path=logs/qry_003.log
#my_db=$sqlite_work
my_db=$sqlite_path
echo DB:$my_db
while IFS='|' read -r col1 col2 col3; do
    brand_code=${col1:5}
    ymd=${col3:0:4}${col3:5:2}${col3:8:2}
    if [ "$ymd" != "$1" ]; then
	continue
    fi
    qry="select ticker_symbol from brand where brand_code='${brand_code}'"
    ticker_symbol=$(sqlite3 $db_opt_cmd $my_db "$qry")
    echo ${brand_code} $ymd $ticker_symbol
    ./hist_read.sh $brand_code $ticker_symbol
    sleep 3s
done < $log_path
