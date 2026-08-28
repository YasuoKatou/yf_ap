#!/bin/bash
source ./env.sh
# 起動引数の日付とログの日付(履歴の最終日付)が一致する銘柄のチャートを作成する
# ログのフォーマット
#   hist_295A|1.047|2026-08-26|2026-08-24
log_path=logs/qry_003.log
#my_db=$sqlite_work
my_db=$sqlite_path
echo DB:$my_db
while IFS='|' read -r col1 col2 col3 col4; do
    brand_code=${col1:5}
    ymd=${col3:0:4}${col3:5:2}${col3:8:2}
    if [ "$ymd" != "$1" ]; then
	continue
    fi
    # 銘柄コードから銘柄を取得
    qry="select brand_name from brand where brand_code='$brand_code'"
    brand_name=$(sqlite3 $db_opt_cmd $sqlite_path "$qry")
    echo "$brand_code : $brand_name"
    # グラフ出力
    python hist_chart.py $brand_code $brand_name
    #sleep 3s
done < $log_path
