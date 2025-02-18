#!/bin/bash

# hbase + YCSB-mixed + Network delay (1ms)
python3 $HOME/workdir/xinda/main.py \
    --sys_name hbase \
    --log_root_dir $HOME/workdir/data/example \
    --data_dir sample_test \
    --fault_type nw \
    --fault_location hbase-regionserver \
    --fault_duration 60 \
    --fault_severity slow-1ms \
    --fault_start_time 60 \
    --bench_exec_time 150 \
    --ycsb_wkl mixed \
    --benchmark ycsb \
    --iter 1

# hbase + YCSB-mixed + network packet loss (10%)
python3 $HOME/workdir/xinda/main.py \
    --sys_name hbase \
    --log_root_dir $HOME/workdir/data/example \
    --data_dir sample_test \
    --fault_type nw \
    --fault_location hbase-regionserver \
    --fault_duration 60 \
    --fault_severity flaky-p10 \
    --fault_start_time 60 \
    --bench_exec_time 150 \
    --ycsb_wkl mixed \
    --benchmark ycsb \
    --iter 1

# hbase + YCSB-mixed + filesystem delay (1ms)
python3 $HOME/workdir/xinda/main.py \
    --sys_name hbase \
    --log_root_dir $HOME/workdir/data/example \
    --data_dir sample_test \
    --fault_type fs \
    --fault_location hbase-regionserver \
    --fault_duration 60 \
    --fault_severity 1000 \
    --fault_start_time 60 \
    --bench_exec_time 150 \
    --ycsb_wkl mixed \
    --benchmark ycsb \
    --iter 1