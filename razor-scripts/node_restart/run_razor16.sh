###################### /data/ruiming/xinda/razor-scripts/node_restart/run_razor16.sh ######################
# $1: workload name
# $2: location (cas1)
function create_dir_if_not_exist() {
    if [ ! -d $1 ]; then
        mkdir $1
        print_red_underlined "[$(date +%s%N), $(date +"%H:%M:%S")] Directory $1 created."
    else
        print_red_underlined "[$(date +%s%N), $(date +"%H:%M:%S")] Directory $1 already exists."
        #exit 1
    fi
}
data_dir=/data/ruiming/data/node_restart
cd $data_dir
log_dir1=r10000_o10000000
log_dir2=${log_dir1}/wkl${1}_logs
create_dir_if_not_exist $log_dir1
create_dir_if_not_exist $log_dir2
meta_log_loc=${data_dir}/${log_dir2}/wkl${1}_meta.log
main_bash_loc=/data/ruiming/xinda/razor-scripts/node_restart/0803.sh 
# status_ary=(slow)

# duration_ary=(25 30)
duration_ary=(30)
start_time_ary=(34 35 36 37 38 39)
for duration in ${duration_ary[@]}; do
    for start_time in ${start_time_ary[@]}; do
        # echo restart-slow3-dur${duration}-${start_time}-$((start_time+duration))
        echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Sourcing cas1 restart-slow3-dur${duration}-${start_time}-$((start_time+duration)).sh now" >> $meta_log_loc
        bash $main_bash_loc $1 10000 10000000 slow $2 restart-slow3-dur${duration}-${start_time}-$((start_time+duration)) slow3
        echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Sourcing cas1 norestart-slow3-dur${duration}-${start_time}-$((start_time+duration)).sh now" >> $meta_log_loc
        bash $main_bash_loc $1 10000 10000000 slow $2 norestart-slow3-dur${duration}-${start_time}-$((start_time+duration)) slow3
    done
done