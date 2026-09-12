#!/bin/bash
# 環境設定を読み込む
source ./env.sh

# sqliteのdbファイルのパスは、環境変数のsqlite_workを参照
my_db=$sqlite_work

# brandテーブルからpaypayカラムに'P'が登録されているbrand_codeを抽出
brand_codes=$(sqlite3 $db_opt_cmd $sqlite_work <<EOF
.parameter set :min_wari 1.05
.read dml/paypay_001.sql
EOF
)
echo $brand_codes

# 取得したbrand_codeを順次hist_chart.shの第1引数として起動し、株価チャートを作成
for brand_code in $brand_codes; do
    if [ -n "$brand_code" ]; then
        ./hist_chart.sh "$brand_code"
    fi
done
