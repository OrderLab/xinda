cd $blockade_dir
########## Config ########
### slow fault
### mu=500, sigma=100
### duration=70
###	start	end	duration	name
### 28	98	70	fault
begin_time=$(date +%s%N)


########## fault 28~98 ########
cur_time=$(($(date +%s%N) - begin_time))
cur_time=$(echo "$cur_time / 10^9" | bc -l | xargs printf "%.3f")
echo "## [$(date +%s%N), $(date +"%H:%M:%S"), $cur_time] Sleep for $(echo "28-$cur_time" | bc ) till next command" >> $rlog_pos
echo "28-$cur_time" | bc | xargs sleep
blockade --config $blockade_file slow $5 500ms 100ms distribution normal
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] fault BEGINs" >> $rlog_pos
cur_time=$(($(date +%s%N) - begin_time))
cur_time=$(echo "$cur_time / 10^9" | bc -l | xargs printf "%.3f")
echo "## [$(date +%s%N), $(date +"%H:%M:%S"), $cur_time] Sleep for $(echo "98-$cur_time" | bc ) till the end" >> $rlog_pos
echo "98-$cur_time" | bc | xargs sleep
blockade --config $blockade_file fast $5
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] fault ENDs" >> $rlog_pos

echo "## mu=500, sigma=100" >> $rlog_pos
echo "## duration=70" >> $rlog_pos
echo "## start	end	duration	name" >> $rlog_pos
echo "## 28	98	70	fault" >> $rlog_pos
