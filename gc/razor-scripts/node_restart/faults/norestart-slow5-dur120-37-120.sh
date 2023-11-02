cd $blockade_dir
########## Config ########
### slow fault
### mu=2000, sigma=200
### duration=120
###	start	end	duration	name
### 37	120	120	fault
begin_time=$(date +%s%N)


########## fault 37~120 ########
cur_time=$(($(date +%s%N) - begin_time))
cur_time=$(echo "$cur_time / 10^9" | bc -l | xargs printf "%.3f")
echo "## [$(date +%s%N), $(date +"%H:%M:%S"), $cur_time] Sleep for $(echo "37-$cur_time" | bc ) till next command" >> $rlog_pos
echo "37-$cur_time" | bc | xargs sleep
blockade --config $blockade_file slow $5 2000ms 200ms distribution normal
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] fault BEGINs" >> $rlog_pos
cur_time=$(($(date +%s%N) - begin_time))
cur_time=$(echo "$cur_time / 10^9" | bc -l | xargs printf "%.3f")
echo "## [$(date +%s%N), $(date +"%H:%M:%S"), $cur_time] Sleep for $(echo "120-$cur_time" | bc ) till the end" >> $rlog_pos
echo "120-$cur_time" | bc | xargs sleep
blockade --config $blockade_file fast $5
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] fault ENDs" >> $rlog_pos

echo "## mu=2000, sigma=200" >> $rlog_pos
echo "## duration=120" >> $rlog_pos
echo "## start	end	duration	name" >> $rlog_pos
echo "## 37	120	120	fault" >> $rlog_pos
