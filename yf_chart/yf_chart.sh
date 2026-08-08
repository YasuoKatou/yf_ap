brand_list_file=./brand_list.csv
ave_short_days=13
ave_long_days=25
history_period=6mo
font_path=/system/fonts/NotoSansCJK-Regular.ttc

py_module=./yf_chart.py

python $py_module \
	--brand_list_file $brand_list_file \
	--ave_short_days $ave_short_days \
	--ave_long_days $ave_long_days \
	--history_period $history_period \
	--font_path $font_path

# for OUKITEL OKT3
#mv ./*.png ~/download/yfinance/graph/
mv ./*.png ~/storage/downloads/yfinance/graph/

# for BLAKVIEW A100
#mv