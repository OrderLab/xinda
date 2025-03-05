#!/bin/bash

# cassandra + YCSB-mixed + 1ms network delay 
python3 $HOME/workdir/xinda/main.py \
    --sys_name cassandra \
    --log_root_dir $HOME/workdir/data/example \
    --data_dir sample_test \
    --fault_type nw \
    --fault_location cas1 \
    --fault_duration 60 \
    --fault_severity slow-1ms \
    --fault_start_time 60 \
    --bench_exec_time 150 \
    --ycsb_wkl mixed \
    --benchmark ycsb \
    --iter 1

# cassandra + YCSB-mixed + 1ms filesystem delay 
python3 $HOME/workdir/xinda/main.py \
    --sys_name cassandra \
    --log_root_dir $HOME/workdir/data/example \
    --data_dir sample_test \
    --fault_type fs \
    --fault_location cas1 \
    --fault_duration 60 \
    --fault_severity 1000 \
    --fault_start_time 60 \
    --bench_exec_time 150 \
    --ycsb_wkl mixed \
    --benchmark ycsb \
    --iter 1

