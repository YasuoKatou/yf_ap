log_path=./logs/db_check.log
python check_db.py > $log_path 2>&1
read -p "チェック結果を先頭から表示"
more $log_path 
read -p "チェック結果の末尾を表示"
tail -n100 $log_path
read -p "grep Error"
grep "error" $log_path
