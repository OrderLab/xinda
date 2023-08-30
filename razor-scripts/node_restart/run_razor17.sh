###################### /data/ruiming/xinda/razor-scripts/node_restart/run_razor17.sh ######################
data_dir=/data/ruiming/data/node_restart/hbase
cd $data_dir
log_dir1=hbase-start0-39
meta_log_loc=${data_dir}/${log_dir1}/meta.log
create_dir_if_not_exist $log_dir1
main_bash_loc=/data/ruiming/xinda/razor-scripts/node_restart/0827.sh 
START_TIME_ARY=(0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39)
location=hbase-regionserver
severity=slow6
wkl=a

# running on razor14, 15, 16, 17
DUR_ARY=(100 110 120)

for duration in ${DUR_ARY[@]}; do
    for start_time in ${START_TIME_ARY[@]}; do
        end_time=$((start_time+duration))
        if [ $end_time -ge 120 ]; then
            end_time=120
        fi
        # echo restart-slow3-dur${duration}-${start_time}-$((start_time+duration))
        echo "## [$(date +%s%N), $(date +"%H:%M:%S")] [RESTART] Sourcing Duration:$duration / Start at $start_time $location restart-${severity}-dur${duration}-${start_time}-${end_time}.sh now" >> $meta_log_loc
        bash $main_bash_loc $wkl 10000 3_ slow $location restart-${severity}-dur${duration}-${start_time}-${end_time} $severity 1 $log_dir1
        echo "## [$(date +%s%N), $(date +"%H:%M:%S")] [NO-RESTART] Sourcing Duration:$duration / Start at $start_time $location norestart-${severity}-dur${duration}-${start_time}-${end_time}.sh now" >> $meta_log_loc
        bash $main_bash_loc $wkl 10000 3_ slow $location restart-${severity}-dur${duration}-${start_time}-${end_time} $severity 1 $log_dir1
    done
done