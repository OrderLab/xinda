#!/bin/bash
# Testing duration, severity and location at fixed timing of 60s
if [ $# -eq 0 ]; then
    echo "No input provided. Exiting."
    exit 1
fi
sys_name=$1
data_dir=rq1_1
start_time=60
duration_ary=(-1 5 10 20 30 40 50 60)
fault_type_ary=(nw fs)
nw_severity=(low high medium)
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
            severity_ary=$nw_severity
            hbase_location=$hbase_nw_location
        else
            severity_ary=$fs_severity
            hbase_location=$hbase_fs_location
        fi
        for severity in ${severity_ary[@]}; do
            case "$sys_name" in
                "cassandra")
                    for location in ${cassandra_location[@]}; do
                        for wkl in ${ycsb_wkl[@]}; do
                            python3 ../main.py --sys_name $sys_name \
                                --data_dir $data_dir \
                                --fault_location $location \
                                --fault_type $fault_type \
                                --fault_duration $duration \
                                --fault_severity $severity \
                                --fault_start_time $start_time \
                                --bench_exec_time 150 \
                                --ycsb_wkl $wkl
                        done
                    done
                    ;;
                "crdb")
                    for location in ${crdb_location[@]}; do
                        for wkl in ${ycsb_wkl_crdb[@]}; do
                            python3 ../main.py --sys_name $sys_name \
                                --data_dir $data_dir \
                                --fault_location $location \
                                --fault_type $fault_type \
                                --fault_duration $duration \
                                --fault_severity $severity \
                                --fault_start_time $start_time \
                                --bench_exec_time 150 \
                                --ycsb_wkl $wkl
                        done
                    done
                    ;;
                *)
                    echo "Unknown option: $first_arg. Exit"
                    exit 1
                    ;;
            esac
        done
    done
done
