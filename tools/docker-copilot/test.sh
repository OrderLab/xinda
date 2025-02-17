#!/bin/bash

for scheme in copilot epaxos multipaxos
do
    echo "$(date) ## $scheme - none" >> meta.log
    python3 $HOME/workdir/xinda/main.py --sys_name copilot --data_dir test --fault_type nw --fault_location replica1 --fault_duration -1 --fault_severity slow-100ms --fault_start_time 5 --bench_exec_time 60 --benchmark copilot --copilot_concurrency 10 --copilot_scheme $scheme --iter 1 --log_root_dir $HOME/workdir/data/copilot_${scheme}
    for sev in slow-100us slow-1ms slow-10ms slow-100ms slow-1s flaky-p1 flaky-p10 flaky-p40 flaky-p70
    do
        echo "$(date) ## $scheme - $sev" >> meta.log
        python3 $HOME/workdir/xinda/main.py --sys_name copilot --data_dir test --fault_type nw --fault_location replica1 --fault_duration 120 --fault_severity $sev --fault_start_time 5 --bench_exec_time 60 --benchmark copilot --copilot_concurrency 10 --copilot_scheme $scheme --iter 1 --log_root_dir $HOME/workdir/data/copilot_${scheme}
    done
done