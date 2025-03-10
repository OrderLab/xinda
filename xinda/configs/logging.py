import os
from xinda.configs.slow_fault import SlowFault
from xinda.configs.benchmark import *
from xinda.configs.reslim import *

class Logging:
    def __init__(self, 
                 sys_name_ : str,
                 data_dir_ : str,
                 fault_ : SlowFault,
                 benchmark_ : Benchmark,
                 iter_ : int,
                 log_root_dir_ : str,
                 version_ : str,
                 reslim_ : ResourceLimit,
                 change_workload: bool,):
        self.create_dir_if_not_exist(log_root_dir_)
        if version_ is None:
            path0 = os.path.join(log_root_dir_, sys_name_)
        else:
            path0 = os.path.join(log_root_dir_, sys_name_+'-'+version_)
        self.create_dir_if_not_exist(path0)
        path1 = os.path.join(path0, data_dir_)
        self.create_dir_if_not_exist(path1)
        path2 = os.path.join(path1, benchmark_.identifier)
        path2 = os.path.join(path2, f"cpu_{reslim_.cpu_limit}", f"mem_{reslim_.mem_limit}")
        self.data_dir = path2
        self.create_dir_if_not_exist(path2)
        iter_ = str(iter_)
        self.iter = iter_

        self.description = fault_.location + '-' + fault_.info + '-' + iter_
        
        if data_dir_ == 'perseus' and sys_name_ == 'hbase':
            self.description = fault_.location + '-' + fault_.info + '-' + 'tc' + str(benchmark_.threadcount) + '-' + iter_

        self.compose = os.path.join(path2, 'compose-' + self.description + ".log")
        self.info = os.path.join(path2, 'info-' + self.description + ".log")
        self.runtime = os.path.join(path2, 'runtime-' + self.description + ".log")
        self.raw = os.path.join(path2, 'raw-' + self.description + ".log")

        # For Cassandra/HBase/etcd (using YCSB)
        self.time_series = os.path.join(path2, 'ts-' + self.description + ".log")
        self.summary = os.path.join(path2, 'sum-' + self.description + ".log")

        # For crdb
        self.crdb_log = os.path.join(path2, 'crlog-' + self.description + ".log")
        self.crdb_health_log = os.path.join(path2, 'health-' + self.description + ".log")
        self.crdb_pebble_log = os.path.join(path2, 'pebble-' + self.description + ".log")
        self.crdb_stderr_log = os.path.join(path2, 'stderr-' + self.description + ".log")

        # For HBase
        self.raw_container = f"/tmp/raw-{self.description}.log"
        self.runtime_container = f"/tmp/runtime-{self.description}.log"
        if change_workload and sys_name_ == 'hbase':
            self.raw_container2 = f"/tmp/raw2-{self.description}.log"
            self.raw2 = os.path.join(path2, 'raw2-' + self.description + ".log")
            self.runtime_container2 = f"/tmp/runtime2-{self.description}.log"
            self.time_series2 = os.path.join(path2, 'ts2-' + self.description + ".log")
            self.summary2 = os.path.join(path2, 'sum2-' + self.description + ".log")
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
            self.raw_load.append(os.path.join(path2, 'raw-load' + str(i) + "-" + self.description + ".log"))
            self.runtime_load.append(os.path.join(path2, 'runtime-load' + str(i) + "-" + self.description + ".log"))
            self.ts_load.append(os.path.join(path2, 'ts-load' + str(i) + "-" + self.description + ".log"))
            self.sum_load.append(os.path.join(path2, 'sum-load' + str(i) + "-" + self.description + ".log"))
            self.raw_run.append(os.path.join(path2, 'raw-run' + str(i) + "-" + self.description + ".log"))
            self.runtime_run.append(os.path.join(path2, 'runtime-run' + str(i) + "-" + self.description + ".log"))
            self.ts_run.append(os.path.join(path2, 'ts-run' + str(i) + "-" + self.description + ".log"))
            self.sum_run.append(os.path.join(path2, 'sum-run' + str(i) + "-" + self.description + ".log"))

        # For Kafka
        self.kafka_producer = os.path.join(path2, 'producer-' + self.description + ".log")
        self.kafka_consumer = os.path.join(path2, 'consumer-' + self.description + ".log")
        self.openmsg_driver = os.path.join(path2, 'driver-' + self.description + ".log")
        self.openmsg_summary = os.path.join(path2, 'sum-' + self.description + ".json")
        self.openmsg_worker1 = os.path.join(path2, 'worker1-' + self.description + ".log")
        self.openmsg_worker2 = os.path.join(path2, 'worker2-' + self.description + ".log")
        
        # For Depfast
        self.depfast_filename = f"raw-{self.description}"
        self.depfast_tarname = f"{self.depfast_filename}.tar"
        self.depfast_tarpath = f"/root/code/depfast/{self.depfast_tarname}"
        self.depfast_misc = 'misc-' + self.description
        self.depfast_summary = 'sum-' + self.description + '.yaml'
        
        # For Copilot
        self.copilot_latency_percentage = self.summary
        self.copilot_aggregated_throughput = self.runtime
        self.copilot_misc = f"misc-{self.description}"
        # self.copilot_misc_
        
    
    def create_dir_if_not_exist(self, path_):
        is_exsit = os.path.exists(path_)
        if not is_exsit:
            os.makedirs(path_)
        else:
            print(f'Directory {path_} already exists!')