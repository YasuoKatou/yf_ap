#!/bin/bash
# 環境設定を読み込む
source ./env.sh

# 第1引数から最小割合を取得。指定がない場合はデフォルト値1.05を設定
min_wari=${1:-1.05}

# 引数が数値（整数または小数）であるかチェック
if [[ ! "$min_wari" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
    echo "割合は数字で指定してください" >&2
    exit 1
fi

# sqliteのdbファイルのパスは、環境変数のsqlite_workを参照
my_db=$sqlite_work

# brandテーブルからpaypayカラムに'P'が登録されているbrand_codeを抽出
brand_codes=$(sqlite3 $db_opt_cmd $sqlite_work <<EOF
.parameter set :min_wari $min_wari
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
