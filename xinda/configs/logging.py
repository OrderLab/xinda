import os
from xinda.configs.slow_fault import SlowFault
from xinda.configs.benchmark import *

class Logging:
    def __init__(self, 
                 sys_name_ : str,
                 data_dir_ : str,
                 fault_ : SlowFault,
                 benchmark_ : Benchmark,
                 iter_ : int,
                 log_root_dir_='/data/ruiming/data/default'):
        path0 = os.path.join(log_root_dir_, sys_name_)
        self.create_dir_if_not_exist(path0)
        path1 = os.path.join(log_root_dir_, sys_name_, data_dir_)
        self.create_dir_if_not_exist(path1)
        path2 = os.path.join(log_root_dir_, sys_name_, data_dir_, benchmark_.workload)
        self.data_dir = path2
        self.create_dir_if_not_exist(path2)
        iter_ = str(iter_)
        self.iter = iter_

        self.compose = os.path.join(path2, 'compose-' + fault_.location + '-' + fault_.info + '-' + iter_ + ".log")
        self.info = os.path.join(path2, 'info-' + fault_.location + '-' + fault_.info + '-' + iter_ + ".log")
        self.runtime = os.path.join(path2, 'runtime-' + fault_.location + '-' + fault_.info + '-' + iter_ + ".log")
        self.raw = os.path.join(path2, 'raw-' + fault_.location + '-' + fault_.info + '-' + iter_ + ".log")

        # For Cassandra/HBase/etcd (using YCSB)
        self.time_series = os.path.join(path2, 'ts-' + fault_.location + '-' + fault_.info + '-' + iter_ + ".log")
        self.summary = os.path.join(path2, 'sum-' + fault_.location + '-' + fault_.info + '-' + iter_ + ".log")

        # For HBase
        self.raw_container = f"/tmp/raw-{fault_.location}-{fault_.info}-{iter_}.log"
        self.runtime_container = f"/tmp/runtime-{fault_.location}-{fault_.info}-{iter_}.log"
        self.raw_load_container = []
        self.runtime_load_container = []
        self.raw_run_container = []
        self.runtime_run_container = []
        self.raw_load = []
        self.runtime_load = []
        self.ts_load = []
        self.sum_load = []
        self.raw_run = []
        self.runtime_run = []
        self.ts_run = []
        self.sum_run = []
        for i in range(10):
            self.raw_load_container.append(f"/tmp/raw-load{i}-{fault_.location}-{fault_.info}-{iter_}.log")
            self.runtime_load_container.append(f"/tmp/runtime-load{i}-{fault_.location}-{fault_.info}-{iter_}.log")
            self.raw_run_container.append(f"/tmp/raw-run{i}-{fault_.location}-{fault_.info}-{iter_}.log")
            self.runtime_run_container.append(f"/tmp/runtime-run{i}-{fault_.location}-{fault_.info}-{iter_}.log")
            self.raw_load.append(os.path.join(path2, 'raw-load' + str(i) + "-" + fault_.location + '-' + fault_.info + '-' + iter_ + ".log"))
            self.runtime_load.append(os.path.join(path2, 'runtime-load' + str(i) + "-" + fault_.location + '-' + fault_.info + '-' + iter_ + ".log"))
            self.ts_load.append(os.path.join(path2, 'ts-load' + str(i) + "-" + fault_.location + '-' + fault_.info + '-' + iter_ + ".log"))
            self.sum_load.append(os.path.join(path2, 'sum-load' + str(i) + "-" + fault_.location + '-' + fault_.info + '-' + iter_ + ".log"))
            self.raw_run.append(os.path.join(path2, 'raw-run' + str(i) + "-" + fault_.location + '-' + fault_.info + '-' + iter_ + ".log"))
            self.runtime_run.append(os.path.join(path2, 'runtime-run' + str(i) + "-" + fault_.location + '-' + fault_.info + '-' + iter_ + ".log"))
            self.ts_run.append(os.path.join(path2, 'ts-run' + str(i) + "-" + fault_.location + '-' + fault_.info + '-' + iter_ + ".log"))
            self.sum_run.append(os.path.join(path2, 'sum-run' + str(i) + "-" + fault_.location + '-' + fault_.info + '-' + iter_ + ".log"))
        # self.raw_container = f"/tmp/raw-{fault_.info}-{iter_}.log"
        # self.runtime_container = f"/tmp/runtime-{fault_.info}-{iter_}.log"

        # For Kafka
        self.kafka_producer = os.path.join(path2, 'producer-' + fault_.location + '-' + fault_.info + '-' + iter_ + ".log")
        self.kafka_consumer = os.path.join(path2, 'consumer-' + fault_.location + '-' + fault_.info + '-' + iter_ + ".log")
        
    
    def create_dir_if_not_exist(self, path_):
        is_exsit = os.path.exists(path_)
        if not is_exsit:
            os.makedirs(path_)
        else:
            print(f'Directory {path_} already exists!')