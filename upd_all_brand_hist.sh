#!/bin/bash
source ./env.sh

today=$(date "+%Y%m%d")
#today=20260728
echo $today
#echo "ls $log_dir/${log_fn1_pfx}_${today}_*.log"
max_no=0
for log_path in $log_dir/${log_fn1_pfx}_${today}_*.log; do
    echo $log_path
    #if [[ "$log_path" =~ ^([a-z]+)_([0-9]+)\.log$ ]]; then
    #if [[ "$log_path" =~ ^(.+)_([0-9]+)\.log$ ]]; then
    if [[ "$log_path" =~ ^(.+)_$today_([0-9]+)\.log$ ]]; then
	no=$(( 10#${BASH_REMATCH[2]} ))
	#no=${BASH_REMATCH[2]}
	#echo $no
	#if [ "$max_no" -ge "$no" ]; then
	if (( max_no < no )); then
	    #echo "max $max_no to $no"
	    max_no=$no
	fi
    fi
done
#echo "today max no : $max_no"
next_no=$((max_no + 1))
#echo "next log no : $next_no"
tmp="0000000000${next_no}"
log_path="$log_dir/${log_fn1_pfx}_${today}_${tmp: -3}.log"
echo "$log_path : next log file"
echo "./init_all_brand_hist.sh > $log_path 2>&1"
./init_all_brand_hist.sh > $log_path 2>&1
