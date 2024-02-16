#!/bin/bash
location=("follower" "leader")
iter=(1 2 3 4 5 6 7 8 9 10)

for loc in "${location[@]}"
do
    for it in "${iter[@]}"
    do
        echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] loc:$loc iter:$it" >> /users/rmlu/workdir/meta.log
        python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir charybdefs-baseline --fault_type fs --fault_location $loc --fault_duration -1 --fault_severity 10000 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter $it --charybdefs_mount_dir /var/lib/docker/cfs_mount/tmp
        echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END]" >> /users/rmlu/workdir/meta.log
    done
done