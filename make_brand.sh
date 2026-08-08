excel_path=./data/data_j.xls
sqlite_path=./data/yfinance.db
table_name=brand
# Excelファイルに登録された銘柄情報をDBに登録する.
echo "Excel  : $excel_path"
echo "sqlite : $sqlite_path"
python make_brand.py \
	-excel_path $excel_path \
	-sqlite_path $sqlite_path \
	-table_name $table_name
# テーブル名の確認
echo -n "データを登録したテーブル : "
sqlite3 $sqlite_path ".table $table_name"
echo schema $table_name as follow
sqlite3 $sqlite_path ".schema $table_name"
# 登録レコード数の確認
echo -n "登録レコード数 : "
sqlite3 -list -noheader $sqlite_path "select count(1) from $table_name"
