# ###################### /data/ruiming/xinda/razor-scripts/node_restart/run_razor16.sh ######################
# function create_dir_if_not_exist() {
#     if [ ! -d $1 ]; then
#         mkdir $1
#         print_red_underlined "[$(date +%s%N), $(date +"%H:%M:%S")] Directory $1 created."
#     else
#         print_red_underlined "[$(date +%s%N), $(date +"%H:%M:%S")] Directory $1 already exists."
#         #exit 1
#     fi
# }
# data_dir=/data/ruiming/data/node_restart/hbase
# create_dir_if_not_exist $data_dir
# cd $data_dir
# log_dir1=hbase-start0-39-slow3
# meta_log_loc=${data_dir}/${log_dir1}/meta.log
# create_dir_if_not_exist $log_dir1
# main_bash_loc=/data/ruiming/xinda/razor-scripts/node_restart/0827.sh 
# START_TIME_ARY=(0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39)
# location=hbase-regionserver
# severity=slow3
# wkl=a

# # running on razor14, 15, 16, 17
# DUR_ARY=(70 80 90)

# for duration in ${DUR_ARY[@]}; do
#     for start_time in ${START_TIME_ARY[@]}; do
#         end_time=$((start_time+duration))
#         if [ $end_time -ge 120 ]; then
#             end_time=120
#         fi
#         echo "## [$(date +%s%N), $(date +"%H:%M:%S")] [RESTART] Sourcing Duration:$duration / Start at $start_time $location restart-${severity}-dur${duration}-${start_time}-${end_time}.sh now" >> $meta_log_loc
#         bash $main_bash_loc $wkl 10000 3_ slow $location restart-${severity}-dur${duration}-${start_time}-${end_time} $severity 1 $log_dir1
#         echo "## [$(date +%s%N), $(date +"%H:%M:%S")] [NO-RESTART] Sourcing Duration:$duration / Start at $start_time $location norestart-${severity}-dur${duration}-${start_time}-${end_time}.sh now" >> $meta_log_loc
#         bash $main_bash_loc $wkl 10000 3_ slow $location norestart-${severity}-dur${duration}-${start_time}-${end_time} $severity 1 $log_dir1
#     done
# done

function create_dir_if_not_exist() {
    if [ ! -d $1 ]; then
        mkdir $1
        print_red_underlined "[$(date +%s%N), $(date +"%H:%M:%S")] Directory $1 created."
    else
        print_red_underlined "[$(date +%s%N), $(date +"%H:%M:%S")] Directory $1 already exists."
        #exit 1
    fi
}
# duration_ary=(5 10 15 20 25 30 35 40)
# duration_ary=(25 30)
# duration_ary=(30)
# scheme_ary=(restart norestart)
# start_time_ary=(0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39)
# identifier=mapre-30

# create_dir_if_not_exist /data/ruiming/data/node_restart/hadoop
# create_dir_if_not_exist /data/ruiming/data/node_restart/hadoop/${identifier}
# meta_log_loc=/data/ruiming/data/node_restart/hadoop/${identifier}/meta.log

# for dur in ${duration_ary[@]}; do
#     for start_time in ${start_time_ary[@]}; do
#         end_time=$((dur+start_time))
#         echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Sourcing restart ${dur}/${start_time}" >> $meta_log_loc
#         bash /data/ruiming/xinda/razor-scripts/node_restart/0825.sh 1_ 2_ 3_ slow datanode restart-slow6-dur${dur}-${start_time}-${end_time} slow6 1 $identifier
#         echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Sourcing norestart ${dur}/${start_time}" >> $meta_log_loc
#         bash /data/ruiming/xinda/razor-scripts/node_restart/0825.sh 1_ 2_ 3_ slow datanode norestart-slow6-dur${dur}-${start_time}-${end_time} slow6 1 $identifier
#     done
# done

dur=30
start_time=26
end_time=$((dur+start_time))
scheme_ary=(restart norestart)
iteration_1st_half=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50)
identifier=mapre-dur30-st26

create_dir_if_not_exist /data/ruiming/data/node_restart/hadoop
create_dir_if_not_exist /data/ruiming/data/node_restart/hadoop/${identifier}
meta_log_loc=/data/ruiming/data/node_restart/hadoop/${identifier}/meta.log

for iter in ${iteration_1st_half[@]}; do
    echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Sourcing restart ${dur}/${start_time} - ${iter}" >> $meta_log_loc
    bash /data/ruiming/xinda/razor-scripts/node_restart/0825.sh 1_ 2_ 3_ slow datanode restart-slow6-dur${dur}-${start_time}-${end_time} slow6 $iter $identifier
    echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Sourcing norestart ${dur}/${start_time} - ${iter}" >> $meta_log_loc
    bash /data/ruiming/xinda/razor-scripts/node_restart/0825.sh 1_ 2_ 3_ slow datanode norestart-slow6-dur${dur}-${start_time}-${end_time} slow6 $iter $identifier
done