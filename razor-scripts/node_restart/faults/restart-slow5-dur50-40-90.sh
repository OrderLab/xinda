cd $blockade_dir
########## Config ########
### slow fault
### mu=2000, sigma=200
### duration=50
###	start	end	duration	name
### 40	90	50	fault
begin_time=$(date +%s%N)


########## fault 40~90 ########
cur_time=$(($(date +%s%N) - begin_time))
cur_time=$(echo "$cur_time / 10^9" | bc -l | xargs printf "%.3f")
echo "## [$(date +%s%N), $(date +"%H:%M:%S"), $cur_time] Sleep for $(echo "40-$cur_time" | bc ) till next command" >> $rlog_pos
echo "40-$cur_time" | bc | xargs sleep
blockade --config $blockade_file slow $5 2000ms 200ms distribution normal
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] fault BEGINs" >> $rlog_pos
cur_time=$(($(date +%s%N) - begin_time))
cur_time=$(echo "$cur_time / 10^9" | bc -l | xargs printf "%.3f")

########## RESTART at 45 ########
echo "## [$(date +%s%N), $(date +"%H:%M:%S"), $cur_time] Sleep for 5s till restart_begin" >> $rlog_pos
sleep 5
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Restarting $5" >> $rlog_pos
docker restart $5
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Restarting completed" >> $rlog_pos

cur_time=$(($(date +%s%N) - begin_time))
cur_time=$(echo "$cur_time / 10^9" | bc -l | xargs printf "%.3f")
if (( $(echo "$cur_time < 90" | bc -l) )); then
	blockade --config $blockade_file slow $5 2000ms 200ms distribution normal
	echo "## [$(date +%s%N), $(date +"%H:%M:%S")] fault resumed" >> $rlog_pos
	########## fault resumed ########
	cur_time=$(($(date +%s%N) - begin_time))
	cur_time=$(echo "$cur_time / 10^9" | bc -l | xargs printf "%.3f")
	echo "## [$(date +%s%N), $(date +"%H:%M:%S"), $cur_time] Sleep for $(echo "90-$cur_time" | bc ) till the end" >> $rlog_pos
	echo "90-$cur_time" | bc | xargs sleep
	blockade --config $blockade_file fast $5
	echo "## [$(date +%s%N), $(date +"%H:%M:%S")] fault ENDs" >> $rlog_pos
fi

echo "## mu=2000, sigma=200" >> $rlog_pos
echo "## duration=50" >> $rlog_pos
echo "## start	end	duration	name" >> $rlog_pos
echo "## 40	90	50	fault" >> $rlog_pos
