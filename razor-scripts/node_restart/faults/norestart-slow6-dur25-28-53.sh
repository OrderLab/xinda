cd $blockade_dir
########## Config ########
### slow fault
### mu=75, sigma=100
### duration=25
###	start	end	duration	name
### 28	53	25	fault
begin_time=$(date +%s%N)


########## fault 28~53 ########
cur_time=$(($(date +%s%N) - begin_time))
cur_time=$(echo "$cur_time / 10^9" | bc -l | xargs printf "%.3f")
echo "## [$(date +%s%N), $(date +"%H:%M:%S"), $cur_time] Sleep for $(echo "28-$cur_time" | bc ) till next command" >> $rlog_pos
echo "28-$cur_time" | bc | xargs sleep
blockade --config $blockade_file slow $5 75ms 100ms distribution normal
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] fault BEGINs" >> $rlog_pos
cur_time=$(($(date +%s%N) - begin_time))
cur_time=$(echo "$cur_time / 10^9" | bc -l | xargs printf "%.3f")
echo "## [$(date +%s%N), $(date +"%H:%M:%S"), $cur_time] Sleep for $(echo "53-$cur_time" | bc ) till the end" >> $rlog_pos
echo "53-$cur_time" | bc | xargs sleep
blockade --config $blockade_file fast $5
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] fault ENDs" >> $rlog_pos

echo "## mu=75, sigma=100" >> $rlog_pos
echo "## duration=25" >> $rlog_pos
echo "## start	end	duration	name" >> $rlog_pos
echo "## 28	53	25	fault" >> $rlog_pos
