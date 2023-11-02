fault_config="--fault_type nw \
    --fault_duration 30 \
    --fault_severity slow3 \
    --fault_start_time 10"
python3 ../main.py --sys_name crdb \
    --data_dir test1 \
    --fault_location roach1 \
    ${fault_config} \
    --bench_exec_time 60 \
    --ycsb_wkl a