import os
import subprocess
import datetime
import time
import yaml
import docker
import sys
import argparse
from xinda.systems import cassandra, crdb, etcd, hbase, mapred, kafka, depfast, copilot
from xinda.configs import logging, slow_fault, tool
from xinda.configs.benchmark import *
from xinda.configs.reslim import *
import traceback


parser = argparse.ArgumentParser(description="Gray failure study on six distributed systems")
parser.add_argument('--sys_name', type = str, required=True,
                    choices=['cassandra', 'hbase', 'hadoop', 'etcd', 'crdb', 'kafka', 'depfast', 'copilot'],
                    help='Name of the distributed systems to be tested.')
parser.add_argument('--data_dir', type = str, required=True,
                    help='Name of data directory to store all the logs')
# Slow fault
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
                    help='[Benchmark] Benchmark duration in seconds')
parser.add_argument('--unique_identifier', type = str, default = None,
                    help='A unique identifier of current experiment')
parser.add_argument('--batch_test_log', type = str, default = None,
                    help='Path to the meta log file of batch test')
parser.add_argument('--if_restart', action='store_true', default=False,
                    help='If we need to restart the system after fault injection')
parser.add_argument('--if_reslim', action='store_true', default=False,
                    help='[Deprecated] If we need to set resource limits on CPU and memory')
parser.add_argument('--if_iaso', action='store_true', default=False,
                    help='If we want to mimic IASO')
parser.add_argument('--cpu_limit', type=str, default=None,
                    help='The number of CPU cores that each container can get at most (e.g., 0.5 or 1 or 5)')
parser.add_argument('--mem_limit', type=str, default=None,
                    help='The size of memory that each container can get at most (e.g., 512M or 1GB or 2GB) ')
# Init
# parser.add_argument('--log_root_dir', type = str, default = '/data/ruiming/data/default',
#                     help='[Init] The root directory to store logs (data)')
# parser.add_argument('--xinda_software_dir', type = str, default = "/data/ruiming/xinda/xinda-software",
#                     help='[Init] The path to xinda-software')
# parser.add_argument('--xinda_tools_dir', type = str, default = "/data/ruiming/xinda/tools",
#                     help='[Init] The path to xinda/tools')
# parser.add_argument('--charybdefs_mount_dir', type = str, default = "/data/ruiming/tmp1",
#                     help='[Init] The path where docker volume and charybdefs use to mount')
# parser.add_argument('--iter', type = str, default = '1',
#                     help='[Init] Iteration of current experiment setup')
parser.add_argument('--log_root_dir', type = str, default = f"{os.path.expanduser('~')}/workdir/data/default",
                    help='[Init] The root directory to store logs (data)')
parser.add_argument('--xinda_software_dir', type = str, default = f"{os.path.expanduser('~')}/workdir/xinda-software",
                    help='[Init] The path to xinda-software')
parser.add_argument('--xinda_tools_dir', type = str, default = f"{os.path.expanduser('~')}/workdir/xinda/tools",
                    help='[Init] The path to xinda/tools')
parser.add_argument('--charybdefs_mount_dir', type = str, default = "/var/lib/docker/cfs_mount/tmp",
                    help='[Init] The path where docker volume and charybdefs use to mount')
parser.add_argument('--iter', type = str, default = '1',
                    help='[Init] Iteration of current experiment setup')
parser.add_argument('--test_script_dir', type = str, default = f"{os.path.expanduser('~')}/workdir/xinda/test_scripts/RQ1_1",
                    help='[Init] The path to test_scripts/RQ1_1')
parser.add_argument('--version', type = str, default = None,
                    help='[Init] Version of the system to be tested')
parser.add_argument('--coverage', action='store_true', default=False,
                    help="[Init] Whether to run coverage study, supported systems: hadoop and etcd")
parser.add_argument('--change_workload', action='store_true', default=False,
                    help="[Init] Whether to change workload at runtime")

# YCSB - Benchmark
parser.add_argument('--ycsb_wkl', type = str, default = 'mixed',
                    help='[Benchmark] YCSB workload type.')
parser.add_argument('--ycsb_recordcount', type = str, default = '10000',
                    help='[Benchmark] Number of records during ycsb-load phase')
parser.add_argument('--ycsb_operationcount', type = str, default = '500000000',
                    help='[Benchmark] Number of operations during ycsb-run phase')
parser.add_argument('--ycsb_measurementtype', type = str, default = 'raw',
                    help='[Benchmark] YCSB measurement type.')
parser.add_argument('--ycsb_status_interval', type = str, default = '1',
                    help='[Benchmark] YCSB measurement itervals (unit: seconds).')
parser.add_argument('--ycsb_columnfamily', type = str, default = 'family',
                    help='[Benchmark] The column family of HBase that YCSB workloads take effect on.')
parser.add_argument('--ycsb_hbase_threadcount', type = int, default = 8,
                    help='[Benchmark] Number of YCSB client threads for HBase.')
parser.add_argument('--ycsb_etcd_threadcount', type = int, default = 300,
                    help='[Benchmark] Number of YCSB client threads for etcd.')
parser.add_argument('--ycsb_etcd_endpoints', type = str, default = 'http://0.0.0.0:2379',
                    help='[Benchmark] Connection strings for the YCSB client to connect etcd.')
parser.add_argument('--ycsb_crdb_max_rate', type = str, default = '0',
                    help='[Benchmark] crdb max_rate (0 for no limits).')
parser.add_argument('--ycsb_crdb_concurrency', type = str, default = '50',
                    help='[Benchmark] The number of concurrent workers.')
parser.add_argument('--ycsb_crdb_load_conn_string', type = str, default = 'postgresql://root@roach3:26257?sslmode=disable',
                    help='[Benchmark] Connection strings during YCSB load phase')
parser.add_argument('--ycsb_crdb_run_conn_string', type = str, default = 'postgresql://root@roach3:26257,roach2:26257,roach1:26257?sslmode=disable',
                    help='[Benchmark] Connection strings during YCSB run phase')
# YCSB - HBASE - Two workloads

parser.add_argument('--ycsb_hbase_threadcount2', type = int, default = 32,
                    help='[Benchmark] Number of YCSB client threads for HBase.')
parser.add_argument('--bench_exec_time2', type = str, default = '150',
                    help='[Benchmark] Benchmark duration in seconds')
parser.add_argument('--ycsb_wkl2', type = str, default = 'writeonly',
                    help='[Benchmark] YCSB workload type.')
parser.add_argument('--ycsb_recordcount2', type = str, default = '1000000',
                    help='[Benchmark] Number of records during ycsb-load phase')
parser.add_argument('--ycsb_columnfamily2', type = str, default = 'family2',
                    help='[Benchmark] The column family of HBase that YCSB workloads take effect on.')

# hadoop - Benchmark
parser.add_argument('--benchmark', type = str, required=True,
                    help='[Benchmark] Specify which benchmark to test the system',
                    choices=['ycsb','mrbench', 'terasort', 'perf_test', 'openmsg', 'ycsb', 'sysbench', 'etcd-official', 'depfast', 'copilot'])
# parser.add_argument('--hadoop_wkl', type = str,
#                     help='[Benchmark] Specify which benchmark to test mapreduce',
#                     choices=['mrbench', 'terasort'])
# mrbench - hadoop - Benchmark
parser.add_argument('--mrbench_num_iter', type = int, default = 10,
                    help='[Benchmark] Number of mrbench jobs running iteratively')
parser.add_argument('--mrbench_num_reduce', type = str, default = '3',
                    help='[Benchmark] Number of mapreduce reduce tasks')
# terasort - hadoop - Benchmark
parser.add_argument('--terasort_num_of_100_byte_rows', type = str, default = '10737418',
                    help='[Benchmark] Number of 100-byte rows to sort in terasort')
parser.add_argument('--terasort_input_dir', type = str, default = '/input',
                    help='[Benchmark] The input directory to store teragen data in HDFS')
parser.add_argument('--terasort_output_dir', type = str, default = '/output',
                    help='[Benchmark] The output directory to store terasort results in HDFS')
# kafka - Benchmark
# parser.add_argument('--kafka_wkl', type = str,
#                     help='[Benchmark] Specify which benchmark to test kafka',
#                     choices=['perf_test', 'openmsg'])
# perf_test - kafka - Benchmark
parser.add_argument('--kafka_replication_factor', type = str, default = '3',
                    help='[Benchmark] Replication factor of performance testing in Kafka')
parser.add_argument('--kafka_topic_partition', type = str, default = '10',
                    help='[Benchmark] Number of topic partitions of performance testing in Kafka')
parser.add_argument('--kafka_throughput_ub', type = int, default = 10000,
                    help='[Benchmark] The upper bound (limit) of throughput in performance testing in Kafka')
parser.add_argument('--kafka_num_msg', type = int, default = 14000000,
                    help='[Benchmark] The number of messages in performance testing in Kafka')
# openmsg - kafka - Benchmark
parser.add_argument('--openmsg_driver', type = str, default = 'kafka-latency',
                    help='[Benchmark] The yaml filename of openmsg kafka driver')
parser.add_argument('--openmsg_workload', type = str, default = 'simple-workload',
                    help='[Benchmark] The yaml filename of openmsg workload')
# crdb - Benchmark
# parser.add_argument('--crdb_wkl', type = str,
#                     help='[Benchmark] Specify which benchmark to test crdb',
#                     choices=['ycsb', 'sysbench'])
# sysbench - crdb - Benchmark
parser.add_argument('--sysbench_lua_scheme', type = str, default='oltp_write_only',
                    help='[Benchmark] The lua scheme to run sysbench workload on crdb')
                    # choices=['oltp_read_only', 'oltp_write_only', 'oltp_read_write'])
parser.add_argument('--sysbench_table_size', type = int, default = 10000,
                    help='[Benchmark] The table size to run sysbench workload on crdb')
parser.add_argument('--sysbench_num_table', type = int, default = 1,
                    help='[Benchmark] Number of tables in a sysbench workload to run on crdb')
parser.add_argument('--sysbench_num_thread', type = int, default = 1,
                    help='[Benchmark] Number of threads to run sysbench workloads on crdb')
parser.add_argument('--sysbench_report_interval', type = int, default = 1,
                    help='[Benchmark] Granularity of sysbench statistics at run-time')
# official-benchmark - etcd - Benchmark
parser.add_argument('--etcd_official_wkl', type = str, default = 'lease-keepalive',
                    choices=['txn-put', 'lease-keepalive', 'range', 'stm', 'watch', 'watch-get'],
                    help='[Benchmark] The benchmark from etcd official benchmarking tool to test etcd')
parser.add_argument('--etcd_official_total', type = int, default = 800000,
                    help='[Benchmark] The total number of requests in an etcd official benchmark')
parser.add_argument('--etcd_official_max_execution_time', type = int, default = 600,
                    help='[Benchmark] The maximum execution time of an etcd official benchmark (unit: seconds)')
parser.add_argument('--etcd_official_isolation', type = str, default = 'r',
                    choices=['r', 'c', 's', 'ss'],
                    help='[Benchmark] The isolation scheme of transactions in official:stm benchmark')
parser.add_argument('--etcd_official_locker', type = str, default = 'stm',
                    choices=['stm', 'lock-client'],
                    help='[Benchmark] The locking scheme of transactions in official:stm benchmark')
parser.add_argument('--etcd_official_num_watchers', type = int, default = 1000000,
                    help='[Benchmark] Number of watchers in benchmark:official-watch-get')
# depfast
parser.add_argument('--depfast_concurrency', type = int, default = 100,
                    help='[Benchmark] The number of client threads in depfast')
parser.add_argument('--depfast_scheme', type = str, default = "fpga_raft",
                    choices=['fpga_raft', 'copilot'],
                    help='[Benchmark] Depfast scheme')
parser.add_argument('--depfast_nclient', type = int, default = 1,
                    help='[Benchmark] Number of client machines')

# copilot
parser.add_argument('--copilot_concurrency', type = int, default = 10,
                    help='[Benchmark] The number of client threads in copilot')
parser.add_argument('--copilot_scheme', type = str, default = "copilot",
                    choices=['latentcopilot', 'epaxos', 'multipaxos', 'copilot'],
                    help='[Benchmark] The tested scheme')
parser.add_argument('--copilot_nclient', type = int, default = 1,
                    help='[Benchmark] Number of client machines')
parser.add_argument('--copilot_trim_ratio', type = str, default = "0",
                    help='[Benchmark] The porportion of data points to be trimmed as noise')


def main(args):
    sys_name = args.sys_name
    if sys_name == 'etcd' and args.fault_location not in ['leader', 'follower']:
        print('Currently etcd only supports leader/follower faults')
        exit(1)
    if args.coverage != False and sys_name not in ['hadoop', 'etcd', 'hbase']:
        print('Currently coverage study only supports hadoop, etcd, and hbase')
        exit(1)
    if args.version is not None and sys_name not in ['hadoop', 'etcd']:
        print('Currently version study only supports hadoop and etcd')
        exit(1)
    if args.cpu_limit is None and args.mem_limit is None:
        args.cpu_limit = "4" # 20 cores in total
        args.mem_limit = "32G" # 128G in total
    elif args.cpu_limit is None or args.mem_limit is None:
        print(f'At least one of cpu_limit ({args.cpu_limit}) or mem_limit ({args.mem_limit}) is None')
        exit(1)
    if args.change_workload and sys_name not in ['hbase']:
        print('Currently only hbase support changing workload at runtime')
        exit(1)
    reslim = ResourceLimit(cpu_limit_ = args.cpu_limit,
                           mem_limit_ = args.mem_limit)

    fault = slow_fault.SlowFault(type_ = args.fault_type,
                        location_ = args.fault_location,
                        duration_ = args.fault_duration,
                        severity_ = args.fault_severity,
                        start_time_ = args.fault_start_time,
                        if_restart_= args.if_restart)
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
                                    data_dir_ = args.data_dir,
                                    log_root_dir_ = args.log_root_dir,
                                    iter_ = args.iter,
                                    xinda_software_dir_ = args.xinda_software_dir,
                                    xinda_tools_dir_ = args.xinda_tools_dir,
                                    charybdefs_mount_dir_ = args.charybdefs_mount_dir,
                                    reslim_ = reslim,
                                    version_=args.version,
                                    if_restart_ = args.if_restart,)
        # sys.test()
    elif sys_name == 'hbase':
        benchmark = YCSB_HBASE(exec_time_ = args.bench_exec_time,
                                workload_ = args.ycsb_wkl,
                                recordcount_ = args.ycsb_recordcount,
                                operationcount_ = args.ycsb_operationcount,
                                measurementtype_ = args.ycsb_measurementtype,
                                status_interval_ = args.ycsb_status_interval,
                                columnfamily_ = args.ycsb_columnfamily,
                                threadcount_ = args.ycsb_hbase_threadcount)
        benchmark2 = YCSB_HBASE(exec_time_ = args.bench_exec_time2,
                                workload_ = args.ycsb_wkl2,
                                recordcount_ = args.ycsb_recordcount2,
                                operationcount_ = args.ycsb_operationcount,
                                measurementtype_ = args.ycsb_measurementtype,
                                status_interval_ = args.ycsb_status_interval,
                                columnfamily_ = args.ycsb_columnfamily2,
                                threadcount_ = args.ycsb_hbase_threadcount2)
        sys = hbase.HBase(sys_name_ = sys_name,
                            fault_ = fault,
                            benchmark_ = benchmark,
                            data_dir_ = args.data_dir,
                            log_root_dir_ = args.log_root_dir,
                            iter_ = args.iter,
                            xinda_software_dir_ = args.xinda_software_dir,
                            xinda_tools_dir_ = args.xinda_tools_dir,
                            charybdefs_mount_dir_ = args.charybdefs_mount_dir,
                            reslim_ = reslim,
                            version_=args.version,
                            if_restart_ = args.if_restart,
                            coverage_ = args.coverage,
                            change_workload_ = args.change_workload,
                            benchmark2_ = benchmark2,
                            if_iaso_ = args.if_iaso)
        # sys.test()
    elif sys_name == 'etcd':
        version = args.version if args.version is not None else '3.5.10'
        if version not in ['3.0.0', '3.4.0', '3.5.10']:
            raise ValueError(f"Version {version} not supported for etcd")

        if args.benchmark == 'ycsb':
            benchmark = YCSB_ETCD(exec_time_ = args.bench_exec_time,
                                    workload_ = args.ycsb_wkl,
                                    recordcount_ = args.ycsb_recordcount,
                                    operationcount_ = args.ycsb_operationcount,
                                    measurementtype_ = args.ycsb_measurementtype,
                                    status_interval_ = args.ycsb_status_interval,
                                    threadcount_ = args.ycsb_etcd_threadcount,
                                    etcd_endpoints_ = args.ycsb_etcd_endpoints)
        elif args.benchmark == 'etcd-official':
            benchmark = OFFICIAL_ETCD(workload_ = args.etcd_official_wkl,
                                    total_ = args.etcd_official_total,
                                    max_execution_time_ = args.etcd_official_max_execution_time,
                                    isolation_ = args.etcd_official_isolation,
                                    stm_locker_ = args.etcd_official_locker,
                                    num_watchers_ = args.etcd_official_num_watchers)
        sys = etcd.Etcd(sys_name_ = sys_name,
                        fault_ = fault,
                        benchmark_ = benchmark,
                        data_dir_ = args.data_dir,
                        log_root_dir_ = args.log_root_dir,
                        iter_ = args.iter,
                        xinda_software_dir_ = args.xinda_software_dir,
                        xinda_tools_dir_ = args.xinda_tools_dir,
                        charybdefs_mount_dir_ = args.charybdefs_mount_dir,
                        reslim_ = reslim,
                        version_=version,
                        if_restart_ = args.if_restart,
                        coverage_ = args.coverage,
                        )
        # sys.test()
    elif sys_name == 'crdb':
        if args.benchmark is None or args.benchmark not in ['ycsb', 'sysbench']:
            print("Need to specify which benchmark to test crdb (--benchmark). Options: ycsb OR sysbench.")
            exit(1)
        if args.ycsb_wkl == 'readonly':
            wkl = 'C'
        elif args.ycsb_wkl == 'mixed':
            wkl = 'A'
        elif args.ycsb_wkl == 'writeonly':
            print('Currently crdb does not support ycsb:writeonly')
            exit(1)
        else:
            wkl = args.ycsb_wkl
        if args.benchmark == 'ycsb':
            benchmark = YCSB_CRDB(exec_time_ = args.bench_exec_time,
                                    workload_ = wkl,
                                    operationcount_ = args.ycsb_operationcount,
                                    max_rate_ = args.ycsb_crdb_max_rate,
                                    concurrency_ = args.ycsb_crdb_concurrency,
                                    status_interval_ = args.ycsb_status_interval,
                                    load_connection_string_ = args.ycsb_crdb_load_conn_string,
                                    run_connection_string_ = args.ycsb_crdb_run_conn_string)
        elif args.benchmark == 'sysbench':
            benchmark = SYSBENCH_CRDB(workload_ = args.benchmark,
                                      lua_scheme_ = args.sysbench_lua_scheme,
                                      table_size_=args.sysbench_table_size,
                                      num_table_=args.sysbench_num_table,
                                      num_thread_=args.sysbench_num_thread,
                                      exec_time_=args.bench_exec_time,
                                      report_interval_=args.sysbench_report_interval
                                      )
        sys = crdb.Crdb(sys_name_ = sys_name,
                        fault_ = fault,
                        benchmark_ = benchmark,
                        data_dir_ = args.data_dir,
                        log_root_dir_ = args.log_root_dir,
                        iter_ = args.iter,
                        xinda_software_dir_ = args.xinda_software_dir,
                        xinda_tools_dir_ = args.xinda_tools_dir,
                        charybdefs_mount_dir_ = args.charybdefs_mount_dir,
                        reslim_ = reslim,
                        version_=args.version,
                        if_restart_ = args.if_restart)
        # sys.test()
    elif sys_name == 'hadoop':
        if args.benchmark is None or args.benchmark not in ['terasort', 'mrbench']:
            print("Need to specify which benchmark to test hadoop (--benchmark). Options: terasort OR mrbench.")
            exit(1)
        if args.benchmark == 'mrbench':
            benchmark = MRBENCH_MAPRED(num_reduces_ = args.mrbench_num_reduce,
                                       num_iter_ = args.mrbench_num_iter)
        elif args.benchmark == 'terasort':
            benchmark = TERASORT_MAPRED(num_of_100_byte_rows_ = args.terasort_num_of_100_byte_rows,
                                        input_dir_ = args.terasort_input_dir,
                                        output_dir_ = args.terasort_output_dir)
        if args.version is None:
            version = '3.3.6'
        elif args.version not in ['3.3.6', '3.2.1', '3.0.0']:
            raise ValueError(f"Version {args.version} not supported for hadoop")
        else:
            version = args.version
        sys = mapred.Mapred(sys_name_ = sys_name,
                            fault_ = fault,
                            benchmark_ = benchmark,
                            data_dir_ = args.data_dir,
                            log_root_dir_ = args.log_root_dir,
                            iter_ = args.iter,
                            xinda_software_dir_ = args.xinda_software_dir,
                            xinda_tools_dir_ = args.xinda_tools_dir,
                            charybdefs_mount_dir_ = args.charybdefs_mount_dir,
                            reslim_ = reslim,
                            version_= version,
                            if_restart_ = args.if_restart,
                            coverage_ = args.coverage, # TODO: implement logic for this
                            )
        # sys.test()    
    elif sys_name == 'kafka':
        if args.benchmark is None or args.benchmark not in ['perf_test', 'openmsg']:
            print("Need to specify which benchmark to test kafka (--benchmark). Options: perf_test OR openmsg.")
            exit(1)
        if args.benchmark == 'perf_test':
            benchmark = PERFTEST_KAFKA(replication_factor_ = args.kafka_replication_factor,
                                       topic_partition_ = args.kafka_topic_partition,
                                       throughput_upper_bound_=args.kafka_throughput_ub,
                                       num_msg_=args.kafka_num_msg,
                                       exec_time_ = args.bench_exec_time)
        elif args.benchmark == 'openmsg':
            benchmark = OPENMSG_KAFKA(driver_=args.openmsg_driver,
                                      workload_file_=args.openmsg_workload,
                                      exec_time_ = args.bench_exec_time)
        sys = kafka.Kafka(  sys_name_ = sys_name,
                            fault_ = fault,
                            benchmark_ = benchmark,
                            data_dir_ = args.data_dir,
                            log_root_dir_ = args.log_root_dir,
                            iter_ = args.iter,
                            xinda_software_dir_ = args.xinda_software_dir,
                            xinda_tools_dir_ = args.xinda_tools_dir,
                            charybdefs_mount_dir_ = args.charybdefs_mount_dir,
                            reslim_ = reslim,
                            version_=args.version,
                            if_restart_ = args.if_restart
                          )
        # sys.test()  
    elif sys_name == 'depfast':
        benchmark = DEFAULT_DEPFAST(exec_time_ = args.bench_exec_time,
                                    concurrency_ = args.depfast_concurrency,
                                    scheme_ = args.depfast_scheme,
                                    nclient_ = args.depfast_nclient)
        sys = depfast.Depfast(sys_name_ = sys_name,
                              fault_ = fault,
                              benchmark_ = benchmark,
                              data_dir_ = args.data_dir,
                              log_root_dir_ = args.log_root_dir,
                              iter_ = args.iter,
                              xinda_software_dir_ = args.xinda_software_dir,
                              xinda_tools_dir_ = args.xinda_tools_dir,
                              charybdefs_mount_dir_ = args.charybdefs_mount_dir,
                              reslim_ = reslim,
                              version_=args.version,
                              if_restart_ = args.if_restart
                              )
    elif sys_name == 'copilot':
        benchmark = DEFAULT_COPILOT(exec_time_ = args.bench_exec_time,
                                    concurrency_ = args.copilot_concurrency,
                                    scheme_ = args.copilot_scheme,
                                    nclient_ = args.copilot_nclient,
                                    trim_ratio_ = args.copilot_trim_ratio)
        sys = copilot.Copilot(sys_name_ = sys_name,
                              fault_ = fault,
                              benchmark_ = benchmark,
                              data_dir_ = args.data_dir,
                              log_root_dir_ = args.log_root_dir,
                              iter_ = args.iter,
                              xinda_software_dir_ = args.xinda_software_dir,
                              xinda_tools_dir_ = args.xinda_tools_dir,
                              charybdefs_mount_dir_ = args.charybdefs_mount_dir,
                              reslim_ = reslim,
                              version_=args.version,
                              if_restart_ = args.if_restart
                              )
    return(sys)

if __name__ == "__main__":
    try:
        args = parser.parse_args()
        cur_command = ' '.join(sys.argv)
        # raise ValueError("This is a test")
        sys = main(args)
        sys.info(f"Current command:\npython3 {cur_command}")
        sys.test()
    # except KeyboardInterrupt:
    #     pass
    except (KeyboardInterrupt, Exception) as e:
        if args.batch_test_log is not None:
            log_file_path = args.batch_test_log
        else:
            log_file_path = './stderr.log'
        with open(log_file_path, 'a') as log_file:
            # if args.unique_identifier is not None:
            #     log_file.write('[' + args.unique_identifier + ']' + '#'*30 + '\n')
            # else:
            #     log_file.write('#'*30+'\n')
            log_file.write('#'*50+'\n')
            cur_ts = int(time.time()*1e9)
            log_file.write(f"[{str(cur_ts)}, {datetime.datetime.now()}]\n")
            log_file.write(f"{cur_command}\n")
            traceback.print_exc(file=log_file)
            log_file.write('#'*50+'\n')
        
# python3 main.py --sys_name cassandra --data_dir test1 --fault_type nw --fault_location cas1 --fault_duration 30 --fault_severity slow3 --fault_start_time 10 --bench_exec_time 60
# python3 main.py --sys_name cassandra --data_dir writeonly --fault_type nw --fault_location cas1 --fault_duration 30 --fault_severity slow3 --fault_start_time 10 --bench_exec_time 60 --ycsb_wkl writeonly

## nw kafka
# python3 main.py --sys_name kafka --data_dir xixi2 --fault_type nw --fault_location kafka1 --fault_duration 30 --fault_severity slow-low --fault_start_time 10 --bench_exec_time 60 --kafka_wkl perf_test
# python3 main.py --sys_name kafka --data_dir xixi2 --fault_type nw --fault_location kafka1 --fault_duration 30 --fault_severity flaky-low --fault_start_time 10 --bench_exec_time 60 --kafka_wkl openmsg
## fs kafka
# python3 main.py --sys_name kafka --data_dir xixi2 --fault_type fs --fault_location kafka1 --fault_duration 30 --fault_severity 1000 --fault_start_time 10 --bench_exec_time 60 --kafka_wkl perf_test

## nw crdb
# python3 main.py --sys_name crdb --data_dir xixi2 --fault_type nw --fault_location roach1 --fault_duration 30 --fault_severity slow-low --fault_start_time 10 --bench_exec_time 60 --ycsb_wkl a --benchmark ycsb
# python3 main.py --sys_name crdb --data_dir xixi2 --fault_type nw --fault_location roach1 --fault_duration 30 --fault_severity flaky-low --fault_start_time 10 --bench_exec_time 60 --benchmark sysbench
## fs crdb
# python3 main.py --sys_name crdb --data_dir xixi2 --fault_type fs --fault_location roach1 --fault_duration 30 --fault_severity 10000 --fault_start_time 10 --bench_exec_time 60 --benchmark sysbench