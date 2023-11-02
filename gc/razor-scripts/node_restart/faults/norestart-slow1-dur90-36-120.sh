cd $blockade_dir
########## Config ########
### slow fault
### mu=30, sigma=10
### duration=90
###	start	end	duration	name
### 36	120	90	fault
begin_time=$(date +%s%N)


########## fault 36~120 ########
cur_time=$(($(date +%s%N) - begin_time))
cur_time=$(echo "$cur_time / 10^9" | bc -l | xargs printf "%.3f")
echo "## [$(date +%s%N), $(date +"%H:%M:%S"), $cur_time] Sleep for $(echo "36-$cur_time" | bc ) till next command" >> $rlog_pos
echo "36-$cur_time" | bc | xargs sleep
blockade --config $blockade_file slow $5 30ms 10ms distribution normal
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] fault BEGINs" >> $rlog_pos
cur_time=$(($(date +%s%N) - begin_time))
cur_time=$(echo "$cur_time / 10^9" | bc -l | xargs printf "%.3f")
echo "## [$(date +%s%N), $(date +"%H:%M:%S"), $cur_time] Sleep for $(echo "120-$cur_time" | bc ) till the end" >> $rlog_pos
echo "120-$cur_time" | bc | xargs sleep
blockade --config $blockade_file fast $5
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] fault ENDs" >> $rlog_pos

echo "## mu=30, sigma=10" >> $rlog_pos
echo "## duration=90" >> $rlog_pos
echo "## start	end	duration	name" >> $rlog_pos
echo "## 36	120	90	fault" >> $rlog_pos
