'''
TestSystem:
    sys_name_: str, 
    fault_: SlowFault, 
    benchmark_: Benchmark,
    data_dir_: str, 
    iter_: int = 1

SlowFault:
    type_ : str, # nw or fs
    location_ : str, # e.g., datanode
    duration_ : int,
    severity_ : str, # "slow3" for nw; "10000" for fs
    start_time_ : int,
    action_ = None

Benchmark:
YCSB_CASSANDRA:
    exec_time_ : str,
    workload_ : str, # a b c d e f
    recordcount_ = '10000',
    operationcount_ = '10000000',
    measurementtype_ = 'ra

YCSB_HBASE:
    exec_time_ : str,
    workload_ : str, # a b c d e f
    recordcount_ = '10000',
    operationcount_ = '10000000',
    measurementtype_ = 'raw',
    status_interval_ = '1',
    columnfamily_ = 'family',

YCSB_ETCD:
    exec_time_ : str,
    workload_ : str, # a b c d e f
    recordcount_ = '10000',
    operationcount_ = '10000000',
    measurementtype_ = 'raw',
    status_interval_ = '1',
    threadcount_ = 1,
    etcd_endpoints_ = 'http://0.0.0.0:2379'

YCSB_CRDB:
    exec_time_ : str, # in seconds
    workload_ : str, # a b c d e f
    operationcount_ = '10000000',
    max_rate_ = '0',
    concurrency_ = '8',
    status_interval_ = '1s',
    load_connection_string_ = 'postgresql://root@roach3:26257?sslmode=disable',
    run_connection_string_ = 'postgresql://root@roach3:26257,roach2:26257,roach1:26257?sslmode=disable'

MRBENCH_MAPRED:
    num_reduces_ = '3',
    num_iter_ = 10
'''

import os
import subprocess
import datetime
import time
import yaml
import docker
import argparse
from xinda.systems import cassandra, crdb, etcd, hbase, mapred, kafka
from xinda.configs import logging, slow_fault, tool
from xinda.configs.benchmark import *


parser = argparse.ArgumentParser(description="Gray failure study on six distributed systems")
parser.add_argument('--sys_name', type = str, required=True,
                    choices=['cassandra', 'hbase', 'hadoop', 'etcd', 'crdb', 'kafka'],
                    help='Name of the distributed systems to be tested.')
parser.add_argument('--data_dir', type = str, required=True,
                    help='Name of data directory to store all the logs')
parser.add_argument('--fault_type', type = str, required=True,
                    choices=['nw','fs','none'],
                    help='[Faults] Types of slow faults to be injected.')
parser.add_argument('--fault_location', type = str, required=True,
                    help='[Faults] Fault injection location')
parser.add_argument('--fault_duration', type = int, required=True,
                    help='[Faults] Fault injection duration')
parser.add_argument('--fault_severity', type = str, required=True,
                    help='[Faults] Fault injection severity')
parser.add_argument('--fault_start_time', type = int, required=True,
                    help='[Faults] Fault injection timing in seconds after the benchmark is running.')
parser.add_argument('--bench_exec_time', type = str, default = '150',
                    help='[Benchmark] Benchmark duration in seconds.')
parser.add_argument('--ycsb_wkl', type = str, default = 'readonly',
                    help='[Benchmark] YCSB workload type.')
parser.add_argument('--ycsb_recordcount', type = str, default = '10000',
                    help='[Benchmark] Number of records during ycsb-load phase.')
parser.add_argument('--ycsb_operationcount', type = str, default = '10000000',
                    help='[Benchmark] Number of operations during ycsb-run phase.')
parser.add_argument('--ycsb_measurementtype', type = str, default = 'raw',
                    help='[Benchmark] YCSB measurement type.')
parser.add_argument('--ycsb_status_interval', type = str, default = '1',
                    help='[Benchmark] YCSB measurement itervals (unit: seconds).')
parser.add_argument('--ycsb_columnfamily', type = str, default = 'family',
                    help='[Benchmark] The column family of HBase that YCSB workloads take effect on.')
parser.add_argument('--ycsb_etcd_threadcount', type = int, default = 300,
                    help='[Benchmark] Number of YCSB client threads for etcd.')
parser.add_argument('--ycsb_etcd_endpoints', type = str, default = 'http://0.0.0.0:2379',
                    help='[Benchmark] Connection strings for the YCSB client to connect etcd.')
parser.add_argument('--ycsb_crdb_max_rate', type = str, default = '0',
                    help='[Benchmark] crdb max_rate (0 for no limits).')
parser.add_argument('--ycsb_crdb_concurrency', type = str, default = '8',
                    help='[Benchmark] The number of concurrent workers.')
parser.add_argument('--ycsb_crdb_load_conn_string', type = str, default = 'postgresql://root@roach3:26257?sslmode=disable',
                    help='[Benchmark] Connection strings during YCSB load phase')
parser.add_argument('--ycsb_crdb_run_conn_string', type = str, default = 'postgresql://root@roach3:26257,roach2:26257,roach1:26257?sslmode=disable',
                    help='[Benchmark] Connection strings during YCSB run phase')
parser.add_argument('--mrbench_num_iter', type = int, default = 10,
                    help='[Benchmark] Number of mrbench jobs running iteratively')
parser.add_argument('--mrbench_num_reduce', type = str, default = '3',
                    help='[Benchmark] Number of mapreduce reduce tasks')

def main():
    args = parser.parse_args()
    sys_name = args.sys_name
    fault = slow_fault.SlowFault(type_ = args.fault_type,
                      location_ = args.fault_location,
                      duration_ = args.fault_duration,
                      severity_ = args.fault_severity,
                      start_time_ = args.fault_start_time)
    # benchmark = Benchmark()
    if sys_name == 'cassandra':
        benchmark = YCSB_CASSANDRA(exec_time_ = args.bench_exec_time,
                                   workload_ = args.ycsb_wkl,
                                   recordcount_ = args.ycsb_recordcount,
                                   operationcount_ = args.ycsb_operationcount,
                                   measurementtype_ = args.ycsb_measurementtype,
                                   status_interval_ = args.ycsb_status_interval
                                   )
        sys = cassandra.Cassandra(sys_name_ = sys_name,
                                  fault_ = fault,
                                  benchmark_ = benchmark,
                                  data_dir_ = args.data_dir)
        sys.test()
    elif sys_name == 'hbase':
        benchmark = YCSB_HBASE(exec_time_ = args.bench_exec_time,
                               workload_ = args.ycsb_wkl,
                               recordcount_ = args.ycsb_recordcount,
                               operationcount_ = args.ycsb_operationcount,
                               measurementtype_ = args.ycsb_measurementtype,
                               status_interval_ = args.ycsb_status_interval,
                               columnfamily_ = args.ycsb_columnfamily)
        sys = hbase.HBase(sys_name_ = sys_name,
                          fault_ = fault,
                          benchmark_ = benchmark,
                          data_dir_ = args.data_dir)
        sys.test()
    elif sys_name == 'etcd':
        benchmark = YCSB_ETCD(exec_time_ = args.bench_exec_time,
                              workload_ = args.ycsb_wkl,
                              recordcount_ = args.ycsb_recordcount,
                              operationcount_ = args.ycsb_operationcount,
                              measurementtype_ = args.ycsb_measurementtype,
                              status_interval_ = args.ycsb_status_interval,
                              threadcount_ = args.ycsb_etcd_threadcount,
                              etcd_endpoints_ = args.ycsb_etcd_endpoints)
        sys = etcd.Etcd(sys_name_ = sys_name,
                        fault_ = fault,
                        benchmark_ = benchmark,
                        data_dir_ = args.data_dir)
        sys.test()
    elif sys_name == 'crdb':
        benchmark = YCSB_CRDB(exec_time_ = args.bench_exec_time,
                              workload_ = args.ycsb_wkl,
                              operationcount_ = args.ycsb_operationcount,
                              max_rate_ = args.ycsb_crdb_max_rate,
                              concurrency_ = args.ycsb_crdb_concurrency,
                              status_interval_ = args.ycsb_status_interval,
                              load_connection_string_ = args.ycsb_crdb_load_conn_string,
                              run_connection_string_ = args.ycsb_crdb_run_conn_string)
        sys = crdb.Crdb(sys_name_ = sys_name,
                        fault_ = fault,
                        benchmark_ = benchmark,
                        data_dir_ = args.data_dir)
        sys.test()
    elif sys_name == 'hadoop':
        benchmark = MRBENCH_MAPRED(num_reduces_ = args.mrbench_num_reduce,
                                   num_iter_ = args.mrbench_num_iter)
        sys = mapred.Mapred(sys_name_ = sys_name,
                            fault_ = fault,
                            benchmark_ = benchmark,
                            data_dir_ = args.data_dir)
        sys.test()
        
    print(args.ycsb_status_interval)
    

if __name__ == "__main__":
    main()

# python3 main.py --sys_name cassandra --data_dir test1 --fault_type nw --fault_location cas1 --fault_duration 30 --fault_severity slow3 --fault_start_time 10 --bench_exec_time 60
# python3 main.py --sys_name cassandra --data_dir writeonly --fault_type nw --fault_location cas1 --fault_duration 30 --fault_severity slow3 --fault_start_time 10 --bench_exec_time 60 --ycsb_wkl writeonly