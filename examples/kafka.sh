#!/bin/bash

# kafka + OpenMessaging + 1ms network delay 
python3 $HOME/workdir/xinda/main.py \
    --sys_name kafka \
    --log_root_dir $HOME/workdir/data/example \
    --data_dir sample_test \
    --fault_type nw \
    --fault_location kafka1 \
    --fault_duration 60 \
    --fault_severity slow-1ms \
    --fault_start_time 60 \
    --bench_exec_time 150 \
    --benchmark openmsg \
    --openmsg_driver kafka-throughput \
    --openmsg_workload 1-topic-1-partition-1kb \
    --iter 1