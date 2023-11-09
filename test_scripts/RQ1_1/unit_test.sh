# python3 generate_test_script.py --sys_name crdb --data_dir rq1_1 --start_time 60 --duration 30  --fault_type fs nw
# python3 generate_test_script.py --sys_name hadoop --data_dir rq1_1 --start_time 60 --duration 30  --fault_type fs nw
# python3 generate_test_script.py --sys_name hbase --data_dir rq1_1 --start_time 60 --duration 30  --fault_type fs nw
# python3 generate_test_script.py --sys_name kafka --data_dir rq1_1 --start_time 60 --duration 30  --fault_type fs nw
# python3 generate_test_script.py --sys_name etcd --data_dir rq1_1 --start_time 60 --duration 30  --fault_type fs nw
# python3 generate_test_script.py --sys_name cassandra --data_dir rq1_1 --start_time 60 --duration 30  --fault_type fs nw

# cassandra
# fs - cas1 - readonly
python3 /users/rmlu/workdir/xinda/main.py --sys_name cassandra --data_dir rq1_1 --fault_type fs --fault_location cas1 --fault_duration 30 --fault_severity 1000 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl readonly --benchmark ycsb
# nw - cas2 - writeonly
python3 /users/rmlu/workdir/xinda/main.py --sys_name cassandra --data_dir rq1_1 --fault_type nw --fault_location cas2 --fault_duration 30 --fault_severity slow-medium --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl writeonly --benchmark ycsb

# crdb
# fs roach1 - sysbench - oltp_delete
python3 /users/rmlu/workdir/xinda/main.py --sys_name crdb --data_dir rq1_1 --fault_type fs --fault_location roach1 --fault_duration 30 --fault_severity 1000 --fault_start_time 60 --bench_exec_time 150 --benchmark sysbench --sysbench_lua_scheme oltp_delete
# nw - roach2 - ycsb - c
python3 /users/rmlu/workdir/xinda/main.py --sys_name crdb --data_dir rq1_1 --fault_type nw --fault_location roach2 --fault_duration 30 --fault_severity slow-medium --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl c --benchmark ycsb

# etcd
# fs etcd0 - ycsb - readonly
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir rq1_1 --fault_type fs --fault_location etcd0 --fault_duration 30 --fault_severity 1000000 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl readonly --benchmark ycsb
# nw etcd1 - ycsb - mixed
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir rq1_1 --fault_type nw --fault_location etcd1 --fault_duration 30 --fault_severity flaky-high --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb

# hadoop
# fs namenode - terasort
python3 /users/rmlu/workdir/xinda/main.py --sys_name hadoop --data_dir rq1_1 --fault_type fs --fault_location namenode --fault_duration 30 --fault_severity 1000 --fault_start_time 60 --bench_exec_time 150 --benchmark terasort
# nw datanode - mrbench
python3 /users/rmlu/workdir/xinda/main.py --sys_name hadoop --data_dir rq1_1 --fault_type nw --fault_location datanode --fault_duration 30 --fault_severity flaky-high --fault_start_time 60 --bench_exec_time 150 --benchmark mrbench

# hbase
# fs - namenode - readonly
python3 /users/rmlu/workdir/xinda/main.py --sys_name hbase --data_dir rq1_1 --fault_type fs --fault_location namenode --fault_duration 30 --fault_severity 1000000 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl readonly --benchmark ycsb
# nw - hbase-regionserver - mixed
python3 /users/rmlu/workdir/xinda/main.py --sys_name hbase --data_dir rq1_1 --fault_type nw --fault_location hbase-regionserver --fault_duration 30 --fault_severity slow-high --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb

# kafka
# fs - kafka1 - perf_test
python3 /users/rmlu/workdir/xinda/main.py --sys_name kafka --data_dir rq1_1 --fault_type fs --fault_location kafka1 --fault_duration 30 --fault_severity 1000 --fault_start_time 60 --bench_exec_time 150 --benchmark perf_test
# nw - kafka2 - perf_test
python3 /users/rmlu/workdir/xinda/main.py --sys_name kafka --data_dir rq1_1 --fault_type nw --fault_location kafka2 --fault_duration 30 --fault_severity flaky-high --fault_start_time 60 --bench_exec_time 150 --benchmark perf_test