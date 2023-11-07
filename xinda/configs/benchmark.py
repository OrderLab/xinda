class Benchmark:
    def __init__(self):
        raise NameError("Please define the specific benchmark")

class YCSB_CASSANDRA(Benchmark):
    def __init__(self, 
                 exec_time_ : str,
                 workload_ : str, # a b c d e f
                 recordcount_ = '10000',
                 operationcount_ = '10000000',
                 measurementtype_ = 'raw',
                 status_interval_ = '1'):
        self.exec_time = exec_time_
        self.workload = workload_
        self.recordcount = recordcount_
        self.operationcount = operationcount_
        self.measurementtype = measurementtype_
        self.status_interval = status_interval_
        self.identifier = 'ycsb-' + workload_

class YCSB_HBASE(Benchmark):
    def __init__(self, 
                 exec_time_ : str,
                #  run_exec_time_ : str,
                #  load_exec_time_ : str,
                 workload_ : str, # a b c d e f
                 recordcount_ = '10000',
                 operationcount_ = '10000000',
                 measurementtype_ = 'raw',
                 status_interval_ = '1',
                 columnfamily_ = 'family'):
        # self.run_exec_time = run_exec_time_
        # self.load_exec_time = load_exec_time_
        self.exec_time = exec_time_
        self.workload = workload_
        self.recordcount = recordcount_
        self.operationcount = operationcount_
        self.measurementtype = measurementtype_
        self.status_interval = status_interval_
        self.columnfamily = columnfamily_
        self.identifier = 'ycsb-' + workload_

class YCSB_ETCD(Benchmark):
    def __init__(self, 
                 exec_time_ : str,
                 workload_ : str, # a b c d e f
                 recordcount_ = '10000',
                 operationcount_ = '10000000',
                 measurementtype_ = 'raw',
                 status_interval_ = '1',
                 threadcount_ = 1,
                 etcd_endpoints_ = 'http://0.0.0.0:2379'):
        self.exec_time = exec_time_
        self.workload = workload_
        self.recordcount = recordcount_
        self.operationcount = operationcount_
        self.measurementtype = measurementtype_
        self.status_interval = status_interval_
        self.threadcount = threadcount_
        self.etcd_endpoints = etcd_endpoints_
        self.identifier = 'ycsb-' + workload_

class YCSB_CRDB(Benchmark):
    def __init__(self, 
                 exec_time_ : str, # in seconds
                 workload_ : str, # a b c d e f
                 operationcount_ = '10000000',
                 benchmark_ = 'ycsb',
                 max_rate_ = '0',
                 concurrency_ = '8',
                 status_interval_ = '1',
                 load_connection_string_ = 'postgresql://root@roach3:26257?sslmode=disable',
                 run_connection_string_ = 'postgresql://root@roach3:26257,roach2:26257,roach1:26257?sslmode=disable'):
        self.exec_time = exec_time_ +'s'
        self.benchmark = benchmark_
        self.workload = workload_.upper()
        self.operationcount = operationcount_
        self.max_rate = max_rate_
        self.concurrency = concurrency_
        self.status_interval = str(status_interval_) + 's'
        self.load_connection_string = load_connection_string_
        self.run_connection_string = run_connection_string_
        self.identifier = 'ycsb-' + workload_

class SYSBENCH_CRDB(Benchmark):
    def __init__(self, 
                 workload_ = 'sysbench',
                 benchmark_ = 'sysbench',
                 lua_scheme_ = 'oltp_write_only',
                 table_size_ = 10000,
                 num_table_ = 1,
                 num_thread_ = 1,
                 exec_time_ = 150,
                 report_interval_ = 1
                 ):
        self.workload = workload_ + "-" + lua_scheme_
        self.benchmark = benchmark_
        self.lua_scheme = lua_scheme_
        self.table_size = table_size_
        self.num_table = num_table_
        self.num_thread = num_thread_
        self.exec_time = exec_time_
        self.report_interval = report_interval_
        self.identifier = 'sysbench-' + lua_scheme_

class MRBENCH_MAPRED(Benchmark):
    def __init__(self, 
                 workload_ = 'mrbench',
                 num_reduces_ = '3',
                 num_iter_ = 10):
        self.workload = workload_
        self.num_reduces = num_reduces_
        self.num_iter = num_iter_
        self.identifier = workload_

class TERASORT_MAPRED(Benchmark):
    def __init__(self, 
                 workload_ = 'terasort',
                 num_of_100_byte_rows_ = '10737418', # 1GB data
                 input_dir_ = '/input', # HDFS DFS location
                 output_dir_ = '/output'): 
        self.workload = workload_
        self.num_of_100_byte_rows = num_of_100_byte_rows_
        self.input_dir = input_dir_
        self.output_dir = output_dir_
        self.identifier = workload_

class PERFTEST_KAFKA(Benchmark):
    def __init__(self, 
                 workload_ = 'perf_test',
                 replication_factor_ = '3',
                 topic_partition_ = '10',
                 topic_title_ = 'test-xinda',
                 throughput_upper_bound_ = 10000,
                 num_msg_ = 14000000,
                 exec_time_ = 150 ):
        self.workload = workload_
        self.benchmark = workload_
        self.replication_factor = replication_factor_
        self.topic_partition = topic_partition_
        self.topic_title = topic_title_
        self.exec_time = int(exec_time_)
        self.throughput_upper_bound = throughput_upper_bound_
        self.num_msg = num_msg_
        self.identifier = workload_

class OPENMSG_KAFKA(Benchmark):
    def __init__(self, 
                 benchmark_ = 'openmsg',
                 workload_ = 'openmsg',
                 driver_ = 'kafka-latency',
                 workload_file_ = 'simple-workload',
                 exec_time_ = 150 ):
        self.benchmark = benchmark_
        self.workload = workload_ + '-' + workload_file_
        self.exec_time = int(exec_time_)
        self.driver = driver_
        self.workload_file = workload_file_
        self.identifier = self.workload
