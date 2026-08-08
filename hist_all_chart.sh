#!/bin/bash

source ./env.sh
qry="select name from sqlite_master where type='table' and name like 'hist%' order by name"
sqlite3 $db_opt_cmd $sqlite_path "$qry" |
while IFS='_' read -r tbl_prefix brand_code
do
    # テーブル名の銘柄コードから、銘柄名とシンボルを取得
    qry="select brand_name from brand where brand_code='$brand_code'"
    brand_name=$(sqlite3 $db_opt_cmd $sqlite_path "$qry")
    echo "$brand_code : $brand_name"
done

#EOF
