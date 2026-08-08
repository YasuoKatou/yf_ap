source ./env.sh
echo "db path        : [$sqlite_path]"
echo "history period : [$hist_period]"

#export brand_code=AAPL
#export target_symbol=AAPL
#export brand_code=9508
#export target_symbol=9508.T
#export brand_code=6902
#export target_symbol=6902.T
#export brand_code=3421
#export target_symbol=3421.T
export brand_code=$code
export target_symbol=$symbol

python history2db.py \
        -sqlite_path $sqlite_path \
        -hist_period $hist_period \
        -brand_code  $brand_code  \
	-target_symbol $target_symbol

#EOF
