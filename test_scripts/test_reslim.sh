# crdb
# python3 /users/rmlu/workdir/xinda/main.py --sys_name crdb --data_dir reslim --fault_type nw --fault_location roach1 --fault_duration 10 --fault_severity slow-50ms --fault_start_time 10 --bench_exec_time 30 --ycsb_wkl a --benchmark ycsb --iter 1 --if_reslim --cpu_limit 3 --mem_limit 512M
# python3 /users/rmlu/workdir/xinda/main.py --sys_name crdb --data_dir reslim --fault_type fs --fault_location roach1 --fault_duration 10 --fault_severity 1000 --fault_start_time 10 --bench_exec_time 30 --ycsb_wkl a --benchmark ycsb --iter 1 --if_reslim --cpu_limit 3 --mem_limit 512M


# etcd
# python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir reslim --fault_type fs --fault_location leader --fault_duration 10 --fault_severity 1000 --fault_start_time 10 --bench_exec_time 30 --ycsb_wkl mixed --benchmark ycsb --iter 1 --if_reslim --cpu_limit 3 --mem_limit 512M
# python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir reslim --fault_type nw --fault_location follower --fault_duration 10 --fault_severity slow-50ms --fault_start_time 10 --bench_exec_time 30 --ycsb_wkl mixed --benchmark ycsb --iter 1 --if_reslim --cpu_limit 3 --mem_limit 512M

# hbase
# MEM=512M will trigger java.lang.OutOfMemoryError: Java heap space
# python3 /users/rmlu/workdir/xinda/main.py --sys_name hbase --data_dir reslim --fault_type fs --fault_location datanode --fault_duration 10 --fault_severity 1000 --fault_start_time 10 --bench_exec_time 30 --ycsb_wkl mixed --benchmark ycsb --iter 1 --if_reslim --cpu_limit 3 --mem_limit 2G
# python3 /users/rmlu/workdir/xinda/main.py --sys_name hbase --data_dir reslim --fault_type fs --fault_location namenode --fault_duration 10 --fault_severity 1000 --fault_start_time 10 --bench_exec_time 30 --ycsb_wkl mixed --benchmark ycsb --iter 1 --if_reslim --cpu_limit 3 --mem_limit 2G
# python3 /users/rmlu/workdir/xinda/main.py --sys_name hbase --data_dir reslim --fault_type nw --fault_location hbase-regionserver --fault_duration 10 --fault_severity slow-50ms --fault_start_time 10 --bench_exec_time 30 --ycsb_wkl mixed --benchmark ycsb --iter 1 --if_reslim --cpu_limit 3 --mem_limit 2G

# kafka
# python3 /users/rmlu/workdir/xinda/main.py --sys_name kafka --data_dir reslim --fault_type nw --fault_location kafka1 --fault_duration 10 --fault_severity slow-30ms --fault_start_time 10 --bench_exec_time 30 --benchmark openmsg --openmsg_driver kafka-big-batches-gzip --openmsg_workload 1-topic-1-partition-1kb --iter 1 --if_reslim --cpu_limit 3 --mem_limit 2G


# cass
python3 /users/rmlu/workdir/xinda/main.py --sys_name cassandra --data_dir reslim --fault_type fs --fault_location cas1 --fault_duration 10 --fault_severity 1000 --fault_start_time 10 --bench_exec_time 30 --ycsb_wkl mixed --benchmark ycsb --iter 1 --if_reslim --cpu_limit 3 --mem_limit 8G
python3 /users/rmlu/workdir/xinda/main.py --sys_name cassandra --data_dir reslim --fault_type nw --fault_location cas1 --fault_duration 10 --fault_severity slow-50ms --fault_start_time 10 --bench_exec_time 30 --ycsb_wkl mixed --benchmark ycsb --iter 1 --if_reslim --cpu_limit 1 --mem_limit 8G
