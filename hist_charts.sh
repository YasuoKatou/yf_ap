#!/bin/bash
source ./env.sh
for brand_code in "$@"; do
    # 銘柄コードから銘柄を取得
    qry="select brand_name from brand where brand_code='$brand_code'"
    brand_name=$(sqlite3 $db_opt_cmd $sqlite_path "$qry")
    echo "$brand_code : $brand_name"
    # グラフ出力
    python hist_chart.py $brand_code $brand_name
done
