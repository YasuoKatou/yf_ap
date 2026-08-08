#!/bin/bash

# お気に入りの銘柄リストファイル
BRAND_List_PATH=./data/brand_list.csv
# 区切り文字（デリミタ）の指定（例：カンマ）
IFS=","

# お気に入りの銘柄リストファイルを1行ずつ読み込む
count=0
while read -r flag code symbol name remarks
do
	count=$((count + 1))
	if [ "$count" -eq 1 ]; then
		# 先頭行は、処理しない（csvヘッダ）
		continue
	fi
	echo $code, $symbol, $name
	source ./history2db.sh
	sleep 3s
done < $BRAND_List_PATH

#EOF
