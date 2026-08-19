#!/bin/bash
source ./env.sh
#
# 銘柄の履歴データを全てDBに登録する
#
source ./env.sh
# 銘柄情報を格納するファイルの接頭辞
prefix1=brand_all_
# １回の起動で処理する最大銘柄数
pmax=100
#pmax=10
# 最後に処理した銘柄コードを保存するファイルのパス
pb_path=$temp_dir/p_brand_code

# ワークディレクトリ内の銘柄情報ファイルを削除する
rm $temp_dir/$prefix1*.csv

# 銘柄情報ファイルを作成する
cond1=''
if [ -f $pb_path ]; then
    echo "ファイルが存在します"
    code=$(head -n 1 $pb_path)
    cond1="where brand_code > '$code'"
fi

tmp_path=$temp_dir/$prefix1$(date "+%Y%m%d%H%M%S").csv
#echo $tmp_path
qry="select brand_code, ticker_symbol, brand_name from brand $cond1 order by brand_code limit $pmax"
sqlite3 $db_opt_csv $sqlite_path "$qry" > $tmp_path

wk_code=''
while IFS=, read brand_code ticker_symbol brand_name; do
    echo "処理する内容: $brand_code $ticker_symbol ${brand_name:1:-2}"
    #
    # 履歴データを取得し、DBに保存する
    ./hist_read.sh $brand_code $ticker_symbol
    #sleep 10s
    sleep 5s
    wk_code="$brand_code"
    if [ -e $stp_fpath1 ]; then
	echo "stop file ${stp_fpath1} found"
	rm $stp_fpath1
	#exit 0
	break
    fi
done < $tmp_path
echo last brand code : $wk_code
echo $wk_code>$pb_path
cat $pb_path
exit 0
