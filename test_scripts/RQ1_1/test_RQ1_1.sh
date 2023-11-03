# Testing duration, severity and location at fixed timing of 60s
if [ $# -eq 0 ]; then
    echo "No input provided. Exiting."
    exit 1
fi
function create_dir_if_not_exist() {
    if [ ! -d $1 ]; then
        mkdir $1
        print_red_underlined "[$(date +%s%N), $(date +"%H:%M:%S")] Directory $1 created."
    else
        print_red_underlined "[$(date +%s%N), $(date +"%H:%M:%S")] Directory $1 already exists."
        #exit 1
    fi
}
# export UID=$(id -u)
# export GID=$(id -g)
main_py=/data/ruiming/xinda/main.py
meta_log_loc=/data/ruiming/xinda/test_scripts/RQ1_1/meta.$(date +"%m.%d.%H.%M.%S").log
export logg=$meta_log_loc
sys_name=$1
data_dir=rq1_1
start_time=60
duration_ary=(-1 5 10 20 30 40 50 60)
fault_type_ary=(fs nw)
nw_severity=(low medium high)
fs_severity=(1000 10000 100000 1000000)
cassandra_location=(cas1 cas2)
crdb_location=(roach1 roach2)
etcd_location=(etcd0 etcd1)
hadoop_location=(datanode namenode historyserver nodemanager)
hbase_fs_location=(datanode namenode)
hbase_nw_location=(datanode namenode hbase-master hbase-regionserver)
ycsb_wkl=(readonly writeonly mixed)
ycsb_wkl_crdb=(a c) # a=mixed, c=readonly

for duration in ${duration_ary[@]}; do
    for fault_type in ${fault_type_ary[@]}; do
        severity_ary=()
        hbase_location=()
        if [ $fault_type == 'nw' ]; then
            severity_ary=("${nw_severity[@]}")
            hbase_location=$hbase_nw_location
        else
            severity_ary=("${fs_severity[@]}")
            hbase_location=$hbase_fs_location
        fi
        echo $severity_ary
        echo $nw_severity
        for severity in ${severity_ary[@]}; do
            echo $severity
            case "$sys_name" in
                "cassandra")
                    for location in ${cassandra_location[@]}; do
                        for wkl in ${ycsb_wkl[@]}; do
                            echo "## [$(date +%s%N), $(date +"%H:%M:%S"), BEGIN] $sys_name ${fault_type}-${severity}-dur${duration}-${location}-st${start_time} workload: $wkl" >> $meta_log_loc
                            python3 $main_py --sys_name $sys_name \
                                --data_dir $data_dir \
                                --fault_location $location \
                                --fault_type $fault_type \
                                --fault_duration $duration \
                                --fault_severity $severity \
                                --fault_start_time $start_time \
                                --bench_exec_time 150 \
                                --ycsb_wkl $wkl
                            echo "## [$(date +%s%N), $(date +"%H:%M:%S"), END]" >> $meta_log_loc
                        done
                    done
                    ;;
                "crdb")
                    for location in ${crdb_location[@]}; do
                        for wkl in ${ycsb_wkl_crdb[@]}; do
                            echo "## [$(date +%s%N), $(date +"%H:%M:%S"), BEGIN] $sys_name ${fault_type}-${severity}-dur${duration}-${location}-st${start_time} workload: $wkl" >> $meta_log_loc
                            python3 $main_py --sys_name $sys_name \
                                --data_dir $data_dir \
                                --fault_location $location \
                                --fault_type $fault_type \
                                --fault_duration $duration \
                                --fault_severity $severity \
                                --fault_start_time $start_time \
                                --bench_exec_time 150 \
                                --ycsb_wkl $wkl
                            echo "## [$(date +%s%N), $(date +"%H:%M:%S"), END]" >> $meta_log_loc
                        done
                    done
                    ;;
                "etcd")
                    for location in ${etcd_location[@]}; do
                        for wkl in ${ycsb_wkl[@]}; do
                            echo "## [$(date +%s%N), $(date +"%H:%M:%S"), BEGIN] $sys_name ${fault_type}-${severity}-dur${duration}-${location}-st${start_time} workload: $wkl" >> $meta_log_loc
                            python3 $main_py --sys_name $sys_name \
                                --data_dir $data_dir \
                                --fault_location $location \
                                --fault_type $fault_type \
                                --fault_duration $duration \
                                --fault_severity $severity \
                                --fault_start_time $start_time \
                                --bench_exec_time 150 \
                                --ycsb_wkl $wkl
                            echo "## [$(date +%s%N), $(date +"%H:%M:%S"), END]" >> $meta_log_loc
                        done
                    done
                    ;;
                "hbase")
                    for location in ${hbase_location[@]}; do
                        for wkl in ${ycsb_wkl[@]}; do
                            echo "## [$(date +%s%N), $(date +"%H:%M:%S"), BEGIN] $sys_name ${fault_type}-${severity}-dur${duration}-${location}-st${start_time} workload: $wkl" >> $meta_log_loc
                            python3 $main_py --sys_name $sys_name \
                                --data_dir $data_dir \
                                --fault_location $location \
                                --fault_type $fault_type \
                                --fault_duration $duration \
                                --fault_severity $severity \
                                --fault_start_time $start_time \
                                --bench_exec_time 150 \
                                --ycsb_wkl $wkl
                            echo "## [$(date +%s%N), $(date +"%H:%M:%S"), END]" >> $meta_log_loc
                        done
                    done
                    ;;
                "hadoop")
                    for location in ${hadoop_location[@]}; do
                        echo "## [$(date +%s%N), $(date +"%H:%M:%S"), BEGIN] $sys_name ${fault_type}-${severity}-dur${duration}-${location}-st${start_time} workload: mrbench" >> $meta_log_loc
                        python3 $main_py --sys_name $sys_name \
                            --data_dir $data_dir \
                            --fault_location $location \
                            --fault_type $fault_type \
                            --fault_duration $duration \
                            --fault_severity $severity \
                            --fault_start_time $start_time \
                            --bench_exec_time 150
                        echo "## [$(date +%s%N), $(date +"%H:%M:%S"), END]" >> $meta_log_loc
                    done
                    ;;
                *)
                    echo "Unknown option: $first_arg. Exit"
                    exit 1
                    ;;
            esac
            if [ $duration -eq -1 ]; then
                echo "## [$(date +%s%N), $(date +"%H:%M:%S"), BREAK] We dont care about different severities for duration=-1" >> $meta_log_loc
                break
            fi
        done
    done
done
