#!/bin/bash

# HDFS + MapReduce + 1ms network delay 
# --fault_location can also be "namenode"
python3 $HOME/workdir/xinda/main.py \
    --sys_name hadoop \
    --log_root_dir $HOME/workdir/data/example \
    --data_dir sample_test \
    --fault_type nw \
    --fault_location datanode \
    --fault_duration 60 \
    --fault_severity slow-1ms \
    --fault_start_time 60 \
    --bench_exec_time 150 \
    --benchmark mrbench \
    --iter 1