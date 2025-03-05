import os
import subprocess
import argparse

class GenerateTestScript():
    def __init__(self,
                 sys_name,
                 scheme,
                 data_dir,
                 path_to_xinda,
                 start_time_ary,
                 duration_ary,
                 fault_type_ary,
                 exec_time,
                 unique_benchmark,
                 fault_type, 
                 iter,):
        self.iter = iter
        self.scheme = scheme
        self.identifier = sys_name
        self.output_file = f"origi_scripts/{self.identifier}.sh"
        self.create_dir_if_not_exist("origi_scripts")
        self.main_py=f"{path_to_xinda}/main.py"
        self.meta_log_loc=f"{path_to_xinda}/examples/meta-{self.identifier}.log"
        self.counter = 0
        sys_name = [sys_name]
        self.sys_name_ary = sys_name
        self.data_dir = data_dir
        self.start_time_ary = start_time_ary
        self.duration_ary = duration_ary
        self.fault_type_ary = fault_type_ary
        self.exec_time = exec_time
        self.unique_benchmark = unique_benchmark
        # location
        self.location_dict = {
            'cassandra': ['cas1'],
            'crdb': ['roach1'],
            'etcd': ['leader', 'follower'],
            'hadoop': ['datanode', 'namenode'],
            'hbase-nw': ['hbase-regionserver'],
            'kafka': ['kafka1']
        }
        # self.ycsb_wkl = ['readonly', 'writeonly', 'mixed']
        self.ycsb_wkl = ['mixed']
        # self.ycsb_wkl_crdb = ['a', 'c']
        self.ycsb_wkl_crdb = ['a']
        self.sysbench_wkl = ['oltp_delete', 
                             'oltp_insert', 
                             'oltp_point_select', 
                             'oltp_read_only', 
                             'oltp_read_write', 
                             'oltp_update_index', 
                             'oltp_update_non_index', 
                             'oltp_write_only', 
                             'select_random_points', 
                             'select_random_ranges' ]
        self.etcd_official = [
            {'lease-keepalive': ['--etcd_official_total 800000']},
            {'range': ['--etcd_official_total 380000']},
            {'txn-put': ['--etcd_official_total 13000']},
            {'watch': ['--etcd_official_total 12000']},
            {'watch-get': ['--etcd_official_num_watchers 1000000']}
        ]
        # severity
        self.severity_dict = {
            'nw': ['slow-100us', 'slow-1ms', 'slow-10ms', 'slow-100ms', 'slow-1s',
                   'flaky-p1', 'flaky-p10', 'flaky-p40', 'flaky-p70'],
            'fs': [1000, 10000, 100000, 1000000]
        }
        if self.scheme == 'danger-zone':
            self.severity_dict = {
                'nw': ['slow-100us', 'slow-200us', 'slow-300us', 'slow-400us', 'slow-500us', 'slow-600us', 'slow-700us', 'slow-800us', 'slow-900us', 
                    'slow-1ms', 'slow-2ms', 'slow-3ms', 'slow-4ms', 'slow-5ms', 'slow-6ms', 'slow-7ms', 'slow-8ms', 'slow-9ms', 
                    'slow-10ms', 'slow-20ms', 'slow-30ms', 'slow-40ms', 'slow-50ms', 'slow-60ms', 'slow-70ms', 'slow-80ms', 'slow-90ms', 
                    'slow-100ms', 'slow-200ms', 'slow-300ms', 'slow-400ms', 'slow-500ms', 'slow-600ms', 'slow-700ms', 'slow-800ms', 'slow-900ms', 'slow-1s',
                    'flaky-p0.1', 'flaky-p0.2', 'flaky-p0.3', 'flaky-p0.4', 'flaky-p0.5', 'flaky-p0.6', 'flaky-p0.7', 'flaky-p0.8', 'flaky-p0.9',
                    'flaky-p1', 'flaky-p2', 'flaky-p3', 'flaky-p4', 'flaky-p5', 'flaky-p6', 'flaky-p7', 'flaky-p8', 'flaky-p9',
                    'flaky-p10', 'flaky-p20', 'flaky-p30', 'flaky-p40', 'flaky-p50', 'flaky-p60', 'flaky-p70', 'flaky-p80', 'flaky-p90'],
                'fs': [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
                    10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000,
                    100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000]
            }
        # resource limits
        self.cpu_limit_ary = ['1','2','5']
        self.mem_limit_ary = ['8G', '16G', '32G']
        # benchmark
        self.benchmark_dict = {
            "hbase": {"ycsb": self.ycsb_wkl},
            "etcd": {"ycsb": self.ycsb_wkl,
                    #  "etcd-official": self.etcd_official
                     },
            "cassandra": {"ycsb": self.ycsb_wkl},
            "crdb": {
                "ycsb": self.ycsb_wkl_crdb,
                # "sysbench": self.sysbench_wkl
                },
            "hadoop": {
                "mrbench": "mrbench",
                "terasort": "terasort"},
            "kafka": {
                "openmsg": {
                    "driver": ["kafka-throughput",
                               "kafka-big-batches-gzip",
                            #    "kafka-sync"
                               ],
                    "workload": ["1-topic-1-partition-1kb",
                                #  "1-topic-16-partitions-1kb",
                                #  "1-topic-100-partitions-1kb"
                                 ]},
                }
        }
    
    def create_dir_if_not_exist(self, path_):
        is_exsit = os.path.exists(path_)
        if not is_exsit:
            os.makedirs(path_)

    def generate(self):
        for sys_name in self.sys_name_ary:
            benchmark_ary = self.benchmark_dict[sys_name]
            for start_time in self.start_time_ary:
                for duration in self.duration_ary:
                    for fault_type in self.fault_type_ary:
                        severity_ary = self.severity_dict[fault_type]
                        if sys_name == 'hbase':
                            location_ary = self.location_dict[f'{sys_name}-{fault_type}']
                        else:
                            location_ary = self.location_dict[sys_name]
                        for severity in severity_ary:
                            for location in location_ary:
                                meta_cmd = [f"python3 {self.main_py}",
                                    f"--sys_name {sys_name}",
                                    f"--data_dir {self.data_dir}",
                                    f"--fault_type {fault_type}",
                                    f"--fault_location {location}",
                                    f"--fault_duration {duration}",
                                    f"--fault_severity {severity}",
                                    f"--fault_start_time {start_time}",
                                    f"--bench_exec_time {self.exec_time}"]
                                if sys_name in ['hbase', 'etcd', 'cassandra', 'crdb']:
                                    for wkl in self.benchmark_dict[sys_name]['ycsb']:
                                        if self.unique_benchmark is None or 'ycsb' == self.unique_benchmark:
                                            cmd = meta_cmd + [
                                                f"--ycsb_wkl {wkl}",
                                                f"--benchmark ycsb"]
                                    if sys_name == 'crdb':
                                        if self.unique_benchmark is None or 'sysbench' == self.unique_benchmark:
                                            # sysbench
                                            for lua_scheme in self.sysbench_wkl:
                                                cmd = meta_cmd + [
                                                    f"--benchmark sysbench",
                                                    f"--sysbench_lua_scheme {lua_scheme}"
                                                ]
                                    if sys_name == 'etcd':
                                        if self.unique_benchmark is None or 'etcd-official' == self.unique_benchmark:
                                            # etcd-official
                                            for item in self.etcd_official:
                                                for wkl_name, flag_list in item.items():
                                                    for flag in flag_list:
                                                        cmd = meta_cmd + [
                                                            f"--benchmark etcd-official",
                                                            f"--etcd_official_wkl {wkl_name}",
                                                            flag
                                                        ]
                                elif sys_name == 'hadoop':
                                    if self.unique_benchmark is None or 'mrbench' == self.unique_benchmark:
                                        # mrbench
                                        cmd = meta_cmd + ["--benchmark mrbench"]
                                    if self.unique_benchmark is None or 'terasort' == self.unique_benchmark:
                                        # terasort
                                        cmd = meta_cmd + ["--benchmark terasort"]
                                elif sys_name == 'kafka':
                                    if self.unique_benchmark is None or 'perf_test' == self.unique_benchmark:
                                        # perf_test
                                        cmd = meta_cmd + ["--benchmark perf_test"]
                                    if self.unique_benchmark is None or 'openmsg' == self.unique_benchmark:
                                        # openmsg
                                        for driver in self.benchmark_dict['kafka']['openmsg']['driver']:
                                            for workload in self.benchmark_dict['kafka']['openmsg']['workload']:
                                                cmd = meta_cmd + [
                                                    f"--benchmark openmsg",
                                                    f"--openmsg_driver {driver}",
                                                    f"--openmsg_workload {workload}"
                                                ]
                                if self.scheme == 'resource-limits':
                                    for cpu_limit in self.cpu_limit_ary:
                                        for mem_limit in self.mem_limit_ary:
                                            reslim_cmd = cmd + [
                                                f"--cpu_limit {cpu_limit}",
                                                f"--mem_limit {mem_limit}"
                                            ]
                                            self.append_to_file(msg=' '.join(reslim_cmd))
                                else:
                                    self.append_to_file(msg=' '.join(cmd))
                            if duration == -1:
                                print("We dont care about different severities for duration=-1")
                                break
        with open(self.output_file, 'r') as file:
            content = file.read()
        content = content.replace('REPLACE_WITH_TOTAL_NUM', f"{self.counter}")
        with open(self.output_file, 'w') as file:
            file.write(content)
        self.output_file = f"origi_scripts/{self.identifier}.sh"
        self.create_dir_if_not_exist("scripts")
        cmd = f"cp {self.output_file} scripts/"
        subprocess.run(cmd, shell=True)
    
    def append_to_file(self, 
                       msg, 
                       filename = None):
        for i in range(1, self.iter+1):
            if filename is None:
                filename = self.output_file
            self.counter = self.counter + 1
            begin_line = f"echo \"## [$(date +%s%N), $(date +\"%Y-%m-%d %H:%M:%S %Z utc%z\"), BEGIN] {self.counter} / REPLACE_WITH_TOTAL_NUM\" >> {self.meta_log_loc}"
            end_line = f"echo \"## [$(date +%s%N), $(date +\"%Y-%m-%d %H:%M:%S %Z utc%z\"), END] {self.counter} / REPLACE_WITH_TOTAL_NUM\" >> {self.meta_log_loc}"
            with open(filename, 'a') as fp:
                fp.write("%s\n" % begin_line)
                fp.write(f"{msg} --iter {i} --unique_identifier {self.counter} --batch_test_log {self.meta_log_loc}\n")
                fp.write("%s\n" % end_line)
                fp.write(f"echo -e '\\n' >> {self.meta_log_loc}")
                fp.write('\n\n')

# def __main__():
parser = argparse.ArgumentParser(description="Generate batch xinda test scripts.")
parser.add_argument('--sys_name', type = str, required=True,
            choices=['cassandra', 'hbase', 'hadoop', 'etcd', 'crdb', 'kafka'],
            help='Name of the distributed systems to be tested.')
parser.add_argument('--scheme', type = str, required=True,
            choices=['sensitivity', 'danger-zone', 'resource-limits'],
            help='Different schemes of the test.')
parser.add_argument('--data_dir', type = str, required=True,    
            help='Name of data directory to store all the logs')
parser.add_argument('--path_to_xinda', type = str, required=True,    
            help='Path to xinda on test nodes')
parser.add_argument('--start_time', type = int, required=True,
                    nargs='+', help='(A list of) start_time. Separated by space. For example: --start_time 10 20 30')
parser.add_argument('--duration', type = int, required=True,
                    nargs='+', help='(A list of) duration. Separated by space. For example: --start_time 10 20 30')
parser.add_argument('--fault_type', type = str, required=True,
                    nargs='+', choices=['nw','fs'],
                    help='(A list of) Types of slow faults to be injected.')
parser.add_argument('--bench_exec_time', type = str, required=False, default = '150',
                    help='Benchmark execution time. Default: 150s')
parser.add_argument('--type', type = str, required=False, default = None,
                    choices=['nw', 'fs', 'nw-flaky', 'nw-slow'],
                    help='Run specific fault type. For example: --type nw')
parser.add_argument('--iter', type = int, required=False, default = 1,
                    help='Number of iterations. Default: 1')
parser.add_argument('--unique_benchmark', type = str, required=False, default = None,
                    help='Only run a specified benchmark. For example: --unique_benchmark ycsb')

args = parser.parse_args()
t = GenerateTestScript(sys_name = args.sys_name,
            scheme = args.scheme,
            data_dir = args.data_dir,
            path_to_xinda = args.path_to_xinda,
            start_time_ary = args.start_time,
            duration_ary = args.duration,
            fault_type_ary = args.fault_type,
            exec_time = args.bench_exec_time,
            unique_benchmark = args.unique_benchmark,
            fault_type = args.type,
            iter = args.iter,)
t.generate()
