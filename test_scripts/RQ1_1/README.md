## exec_time sketch
Below is the estimated (sketch) execution time for each system per fault/benchmark setup.
| System | exec_time (min) |
| --- | --- |
| crdb | 3.5 |
| etcd | 3 |
| hadoop | 5 |
| cassandra | 7 |
| hbase | 4.5 |
| kafka | 3.3 |

## Comments
The total combination of experiment setups can be calculated as follows:
$$[fault\ type]\times[fault\ severity]\times[fault\ duration]\times[fault\ start\ time]\times[fault\ location]\times[Number\ of\ benchmarks/workloads]$$

For a full RQ1_1 test on crdb, we need to run
$$2\times10\times8\times1\times2\times12=3840,$$
which is really a 'nightmare': we need $3.5\times3840/60\approx224\ machine\ hours$, not to mention the time to analyze the results 🤔

> Iterating through all possible combinations of variables is indeed time-consuming. But we can't say for sure that these variables are not correlated: e.g., only some combinations could trigger a certain system behavior. I think the variable that is most easily excluded is $[fault\ location]$, as the nodes do not differ from each other in most distributed systems (except for hadoop and hbase). We can first try different values of $[fault\ location]$, make sure they won't affect results in some systems, and thus simplifying the equation step by step.

- [ ] Another thing is that we need to tune the parameters so that the system performance is reasonably good.

## Usage

```
python3 generate_test_script.py \
--sys_name <SYSNAME> \
--data_dir rq1_1 \
--start_time <LIST_OF_START_TIME> \
--duration <LIST_OF_DURATION> \
--fault_type <fs and/or nw>

# For example
python3 generate_test_script.py --sys_name crdb --data_dir rq1_1 --start_time 60 --duration -1 30  --fault_type fs nw

# python3 generate_test_script.py --sys_name hadoop --data_dir newv --start_time 10 --duration 50  --fault_type nw

# A new bash script will be generated under this folder. To run the test script
bash crdb-fs-nw-dur--1-30.sh
```

## RQ 1-1

```shell
python3 rq1_1.py --sys_name crdb --data_dir rq1_1 --start_time 60 --duration 30  --fault_type fs nw --unique_benchmark ycsb --iter 50
python3 rq1_1.py --sys_name etcd --data_dir rq1_1 --start_time 60 --duration 30  --fault_type fs nw --unique_benchmark ycsb --iter 50
python3 rq1_1.py --sys_name hadoop --data_dir rq1_1 --start_time 60 --duration 30  --fault_type fs nw --iter 50 --unique_benchmark terasort
python3 rq1_1.py --sys_name cassandra --data_dir rq1_1 --start_time 60 --duration 30  --fault_type nw --unique_benchmark ycsb --iter 50
python3 rq1_1.py --sys_name kafka --data_dir rq1_1 --start_time 60 --duration 30  --fault_type nw --unique_benchmark openmsg --iter 50
python3 rq1_1.py --sys_name hbase --data_dir rq1_1 --start_time 60 --duration 30  --fault_type nw --unique_benchmark ycsb --iter 50
```

## RQ 1-2

mrbench
```
python3 generate_test_script.py --sys_name hadoop --data_dir rq1_2 --start_time 30 31 32 33 --duration 5 10 20 --fault_type nw fs --unique_benchmark mrbench
python3 generate_test_script.py --sys_name hadoop --data_dir rq1_2 --start_time 34 35 36 37 --duration 5 10 20 --fault_type nw fs --unique_benchmark mrbench
python3 generate_test_script.py --sys_name hadoop --data_dir rq1_2 --start_time 38 39 40 41 --duration 5 10 20 --fault_type nw fs --unique_benchmark mrbench
python3 generate_test_script.py --sys_name hadoop --data_dir rq1_2 --start_time 42 43 44 45 --duration 5 10 20 --fault_type nw fs --unique_benchmark mrbench
python3 generate_test_script.py --sys_name hadoop --data_dir rq1_2 --start_time 46 47 48 49 --duration 5 10 20 --fault_type nw fs --unique_benchmark mrbench
```

## RQ 1-4
Test the slow-fault-tolerant limit
```
python3 generate_test_script.py --sys_name crdb --data_dir rq1_4 --start_time 60 --duration 1200 --bench_exec_time 1500 --fault_type nw fs
python3 generate_test_script.py --sys_name cassandra --data_dir rq1_4 --start_time 60 --duration 1200 --bench_exec_time 1500 --fault_type nw fs
python3 generate_test_script.py --sys_name hbase --data_dir rq1_4 --start_time 60 --duration 1200 --bench_exec_time 1500 --fault_type nw fs
python3 generate_test_script.py --sys_name etcd --data_dir rq1_4 --start_time 60 --duration 1200 --bench_exec_time 1500 --fault_type nw fs --unique_benchmark ycsb
python3 generate_test_script.py --sys_name hadoop --data_dir rq1_4 --start_time 60 --duration 1200 --bench_exec_time 1500 --fault_type nw fs
python3 generate_test_script.py --sys_name kafka --data_dir rq1_4 --start_time 60 --duration 1200 --bench_exec_time 1500 --fault_type nw
```

## RQ 1-5 Actions + RQ 1-6 Residual Effects

`--if_restart` flag to enable restart (right after 5s of slow fault)

Corner cases:
* For kafka, we only inject nw-related faults
* For HBase, we only inject nw-related faults. This is because HBase use HDFS for storage and thus fs-related faults are injected to HDFS nodes only. In this case, we do not need to explore the same topic again.
* For HDFS, we only restart the datanode. Restarting the namenode will result in service downtime. TODO => enable High Availability mode with a secondary namenode for HDFS + get the latest stable version.

```
python3 generate_test_script.py --sys_name cassandra --data_dir restart --start_time 60 --duration 5 10 20 30 40 --fault_type nw fs --bench_exec_time 300 --if_restart
python3 generate_test_script.py --sys_name crdb --data_dir restart --start_time 60 --duration 5 10 20 30 40 --fault_type nw fs --bench_exec_time 300 --if_restart
python3 generate_test_script.py --sys_name etcd --data_dir restart --start_time 60 --duration 5 10 20 30 40 --fault_type nw fs --bench_exec_time 300 --if_restart
python3 generate_test_script.py --sys_name kafka --data_dir restart --start_time 60 --duration 5 10 20 30 40 --fault_type nw --bench_exec_time 300 --if_restart
python3 generate_test_script.py --sys_name hbase --data_dir restart --start_time 60 --duration 5 10 20 30 40 --fault_type nw --bench_exec_time 300 --if_restart
python3 generate_test_script.py --sys_name hadoop --data_dir restart --start_time 60 --duration 5 10 20 30 40 --fault_type nw fs --bench_exec_time 300 --if_restart
```