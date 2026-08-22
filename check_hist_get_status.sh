
#!/bin/bash
log_folder=logs
log_pattern=update_hist_*.log
log_file=$(ls -t ./$log_folder/$log_pattern | head -n 1)
#echo $log_file
grep records $log_file | wc -l

