#!/bin/bash

# CRDB + YCSB-mixed + 1ms network delay 
python3 $HOME/workdir/xinda/main.py \
    --sys_name crdb \
    --log_root_dir $HOME/workdir/data/example \
    --data_dir sample_test \
    --fault_type nw \
    --fault_location roach1 \
    --fault_duration 60 \
    --fault_severity slow-1ms \
    --fault_start_time 60 \
    --bench_exec_time 150 \
    --ycsb_wkl a \
    --benchmark ycsb \
    --iter 1

# CRDB + SysBench + 1ms filesystem delay 
python3 $HOME/workdir/xinda/main.py \
    --sys_name crdb \
    --log_root_dir $HOME/workdir/data/example \
    --data_dir sample_test \
    --fault_type fs \
    --fault_location roach1 \
    --fault_duration 60 \
    --fault_severity 1000 \
    --fault_start_time 60 \
    --bench_exec_time 150 \
    --benchmark sysbench \
    --sysbench_lua_scheme oltp_read_write \
    --iter 1