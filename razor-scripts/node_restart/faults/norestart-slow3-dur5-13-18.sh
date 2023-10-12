cd $blockade_dir
########## Config ########
### slow fault
### mu=500, sigma=100
### duration=5
###	start	end	duration	name
### 13	18	5	fault
begin_time=$(date +%s%N)


########## fault 13~18 ########
cur_time=$(($(date +%s%N) - begin_time))
cur_time=$(echo "$cur_time / 10^9" | bc -l | xargs printf "%.3f")
echo "## [$(date +%s%N), $(date +"%H:%M:%S"), $cur_time] Sleep for $(echo "13-$cur_time" | bc ) till next command" >> $rlog_pos
echo "13-$cur_time" | bc | xargs sleep
blockade --config $blockade_file slow $5 500ms 100ms distribution normal
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] fault BEGINs" >> $rlog_pos
cur_time=$(($(date +%s%N) - begin_time))
cur_time=$(echo "$cur_time / 10^9" | bc -l | xargs printf "%.3f")
echo "## [$(date +%s%N), $(date +"%H:%M:%S"), $cur_time] Sleep for $(echo "18-$cur_time" | bc ) till the end" >> $rlog_pos
echo "18-$cur_time" | bc | xargs sleep
blockade --config $blockade_file fast $5
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] fault ENDs" >> $rlog_pos

echo "## mu=500, sigma=100" >> $rlog_pos
echo "## duration=5" >> $rlog_pos
echo "## start	end	duration	name" >> $rlog_pos
echo "## 13	18	5	fault" >> $rlog_pos
