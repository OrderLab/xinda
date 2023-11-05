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

class YCSB_CRDB(Benchmark):
    def __init__(self, 
                 exec_time_ : str, # in seconds
                 workload_ : str, # a b c d e f
                 operationcount_ = '10000000',
                 max_rate_ = '0',
                 concurrency_ = '8',
                 status_interval_ = '1',
                 load_connection_string_ = 'postgresql://root@roach3:26257?sslmode=disable',
                 run_connection_string_ = 'postgresql://root@roach3:26257,roach2:26257,roach1:26257?sslmode=disable'):
        self.exec_time = exec_time_ +'s'
        self.workload = workload_.upper()
        self.operationcount = operationcount_
        self.max_rate = max_rate_
        self.concurrency = concurrency_
        self.status_interval = str(status_interval_) + 's'
        self.load_connection_string = load_connection_string_
        self.run_connection_string = run_connection_string_

class MRBENCH_MAPRED(Benchmark):
    def __init__(self, 
                 workload_ = 'mrbench',
                 num_reduces_ = '3',
                 num_iter_ = 10):
        self.workload = workload_
        self.num_reduces = num_reduces_
        self.num_iter = num_iter_

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

class KAFKA(Benchmark):
    def __init__(self, 
                 workload_ = 'perf_test',
                 replication_factor_ = '4',
                 topic_partition_ = '10',
                 topic_title_ = 'test-xinda'):
        self.workload = workload_
        self.replication_factor = replication_factor_
        self.topic_partition = topic_partition_
        self.topic_title = topic_title_
