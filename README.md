To change workload at runtime (only supports HBase), play with `--change_worklad`, `--ycsb_wkl2`, `--ycsb_hbase_threadcount2`, `--bench_exec_time2`.
```shell
python3 /users/rmlu/workdir/xinda/main.py --sys_name hbase --data_dir tool --fault_type nw --fault_location hbase-regionserver --fault_duration -1 --fault_severity slow-10ms --fault_start_time 20 --change_workload --benchmark ycsb --iter 1 --log_root_dir /users/rmlu/workdir/data/0909_0421 \
    --bench_exec_time 60 --ycsb_wkl mixed --ycsb_hbase_threadcount 1 --ycsb_recordcount 10000 --ycsb_columnfamily family \
    --bench_exec_time2 60 --ycsb_wkl2 writeonly --ycsb_hbase_threadcount2 32 --ycsb_recordcount2 1000000 --ycsb_columnfamily2 family2
```


To reset/clean up the working environment for next `xinda` test:
```shell
python3 cleanup.py
```

To run a sample `xinda` test:
```shell
python3 main.py --sys_name hbase --data_dir rq1_1 --fault_type nw --fault_location hbase-regionserver --fault_duration 60 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 1
```

To process the raw exp data:
```shell
# NOTE: the internal raw exp data path should follow:
# exp_name/<sys_name>/<tag>/<benchmark>/<num_cpu>/<num_mem>
# e.g., concurrent_tool/hbase/tool/ycsb-mixed/cpu_4/mem_32G/
python3 ./analyze/process.py -d <path_to_concurrent_tool>
```

* `./analyze` contains scripts to process raw experiment data
* `./cloudlab-ansible` contains scripts to initialize and config CloudLab servers from scratch
* `./gc` namely garbage collection
* `./test_scripts` contains the shell scripts to run experiments
* `./tools` contains blockade files and docker compose files for each system
* `./xinda-software`: :warning: deprecated and no longer updated. We git-clone xinda-software in a separate path On CloudLab servers
* `./xinda` is the code base of testing 6 distributed systems with different benchmarks and slow faults
