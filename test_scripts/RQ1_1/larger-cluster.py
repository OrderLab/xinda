import os
import subprocess
import yaml
import time
import datetime
import argparse
import socket

class GenerateTestScript():
    def __init__(self,
                 sys_name,
                 data_dir,
                 start_time_ary,
                 duration_ary,
                 fault_type_ary,
                 exec_time,
                 unique_benchmark,
                 disable_port_check,
                 if_restart,
                 severity, 
                 iter,
                 version = None,
                 coverage_enabled: bool = False,):
        self.iter = iter
        # self.output_file=f"{os.path.expanduser('~')}/xinda/test_scripts/RQ1_1/commands.txt"
        if unique_benchmark is not None:
            self.identifier = f"{sys_name}-{'-'.join(fault_type_ary)}-dur-{'-'.join([str(item) for item in duration_ary])}-st-{'-'.join([str(item) for item in start_time_ary])}-{unique_benchmark}-{iter}iter"
        else:
            self.identifier = f"{sys_name}-{'-'.join(fault_type_ary)}-dur-{'-'.join([str(item) for item in duration_ary])}-st-{'-'.join([str(item) for item in start_time_ary])}-{iter}iter"
        if if_restart:
            self.identifier = f"restart-{self.identifier}"
        else:
            self.identifier = f"norestart-{self.identifier}"
        self.output_file = self.identifier + ".sh"
        # self.main_py=f"{os.path.expanduser('~')}/workdir/xinda/main.py"
        self.main_py=f"/users/rmlu/workdir/xinda/main.py"
        self.counter = 0
        # self.meta_log_loc=f"{os.path.expanduser('~')}/workdir/xinda/test_scripts/RQ1_1/meta.{datetime.datetime.now().strftime('%m.%d.%H.%M.%S')}.log"
        self.meta_log_loc=f"/users/rmlu/workdir/xinda/test_scripts/RQ1_1/meta-{self.identifier}.log"
        if sys_name == 'all':
            sys_name = ['crdb', 'cassandra', 'hbase', 'kafka', 'etcd', 'hadoop']
        else:
            sys_name = [sys_name]
        self.sys_name_ary = sys_name
        self.data_dir = data_dir
        self.start_time_ary = start_time_ary
        self.duration_ary = duration_ary
        self.fault_type_ary = fault_type_ary
        self.exec_time = exec_time
        self.unique_benchmark = unique_benchmark
        self.if_restart = if_restart
        self.version = version
        self.coverage_enabled = coverage_enabled
        # location
        if if_restart:
            self.location_dict = {
                # 'cassandra': ['cas1', 'cas2'],
                # 'crdb': ['roach1', 'roach2'],
                'cassandra': ['cas1'],
                'crdb': ['roach1'],
                'etcd': ['leader', 'follower'],
                'hadoop': ['datanode', 'namenode'],
                'hbase-fs': ['datanode', 'namenode'],
                'hbase-nw': ['hbase-master','hbase-regionserver'],
                'kafka': ['kafka1', 'kafka2']
            }
        else:
            self.location_dict = {
                # 'cassandra': ['cas1', 'cas2'],
                # 'crdb': ['roach1', 'roach2'],
                'cassandra': ['cas1'],
                'crdb': ['roach1'],
                'etcd': ['leader', 'follower'],
                # 'hadoop': ['datanode', 'namenode'],
                # 'hbase-fs': ['datanode', 'namenode'],
                # 'hbase-nw': ['datanode', 'namenode', 'hbase-master','hbase-regionserver'],
                'hbase-nw': ['hbase-regionserver'],
                # 'kafka': ['kafka1', 'kafka2']
                'kafka': ['kafka1']
            }
        self.ycsb_wkl = ['readonly', 'writeonly', 'mixed']
        self.ycsb_wkl_crdb = ['a', 'c', 'g']
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
            # {'stm': ['--etcd_official_total 380000 --etcd_official_isolation r --etcd_official_locker stm',
            #          '--etcd_official_total 130000 --etcd_official_isolation s --etcd_official_locker stm',
            #          '--etcd_official_total 400000 --etcd_official_isolation c --etcd_official_locker stm',
            #          '--etcd_official_total 130000 --etcd_official_isolation ss --etcd_official_locker stm',
            #          '--etcd_official_total 6000 --etcd_official_isolation r --etcd_official_locker lock-client',
            #          '--etcd_official_total 6000 --etcd_official_isolation s --etcd_official_locker lock-client',
            #          '--etcd_official_total 6000 --etcd_official_isolation c --etcd_official_locker lock-client',
            #          '--etcd_official_total 6000 --etcd_official_isolation ss --etcd_official_locker lock-client']},
            {'txn-put': ['--etcd_official_total 13000']},
            {'watch': ['--etcd_official_total 12000']},
            {'watch-get': ['--etcd_official_num_watchers 1000000']}
        ]
        # severity
        self.severity_dict = {
            # 'nw': ['slow-200us', 'slow-300us', 'slow-400us', 'slow-500us', 'slow-600us', 'slow-700us', 'slow-800us', 'slow-900us', 'slow-1.5ms', 'slow-2ms','slow-2.5ms', 'slow-3ms', 'slow-3.5ms', 'slow-4ms', 'slow-4.5ms', 'slow-5ms', 'slow-5.5ms', 'slow-6ms', 'slow-6.5ms', 'slow-7ms', 'slow-7.5ms', 'slow-8ms', 'slow-8.5ms', 'slow-9ms', 'slow-9.5ms'],
            # 'nw': ['slow-100us', 'slow-200us', 'slow-300us', 'slow-400us', 'slow-500us', 'slow-600us', 'slow-700us', 'slow-800us', 'slow-900us',  'slow-1ms', 'slow-2ms', 'slow-3ms', 'slow-4ms', 'slow-5ms', 'slow-6ms', 'slow-7ms', 'slow-8ms', 'slow-9ms', 'slow-10ms'],
            'nw': ['flaky-p1', 'flaky-p10', 'flaky-p40', 'flaky-p70', 
                   'slow-100us','slow-500us','slow-1ms','slow-5ms', 'slow-10ms', 'slow-50ms','slow-100ms', 'slow-300ms', 'slow-500ms',  'slow-700ms', 'slow-1s'],  
            'fs': [1000, 10000, 100000, 1000000]
        }
        # if severity is not None:
        #     if severity == 'nw':
        #         self.severity_dict = {'nw': self.severity_dict['nw']}
        #     elif severity == 'fs':
        #         self.severity_dict = {'fs': self.severity_dict['fs']}
        #     elif severity == 'nw-flaky':
        #         self.severity_dict = {'nw': ['flaky-p10', 'flaky-p40', 'flaky-p70']}
        #     elif severity == 'nw-slow':
        #         self.severity_dict = {'nw': ['slow-100us', 'slow-1ms', 'slow-10ms', 'slow-100ms']}
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
                                if self.version is not None:
                                    meta_cmd.append(f"--version {self.version}")
                                if self.coverage_enabled:
                                    meta_cmd.append("--coverage")
                                if self.if_restart:
                                    meta_cmd.append("--if_restart")
                                if sys_name in ['hbase', 'etcd', 'cassandra', 'crdb']:
                                    for wkl in self.benchmark_dict[sys_name]['ycsb']:
                                        if self.unique_benchmark is None or 'ycsb' == self.unique_benchmark:
                                            cmd = meta_cmd + [
                                                f"--ycsb_wkl {wkl}",
                                                f"--benchmark ycsb"]
                                            self.append_to_file(msg=' '.join(cmd))
                                    if sys_name == 'crdb':
                                        if self.unique_benchmark is None or 'sysbench' == self.unique_benchmark:
                                            # sysbench
                                            for lua_scheme in self.sysbench_wkl:
                                                cmd = meta_cmd + [
                                                    f"--benchmark sysbench",
                                                    f"--sysbench_lua_scheme {lua_scheme}"
                                                ]
                                                self.append_to_file(msg=' '.join(cmd))
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
                                                        self.append_to_file(msg=' '.join(cmd))
                                            
                                elif sys_name == 'hadoop':
                                    if self.if_restart and location == 'namenode':
                                        pass
                                    else:
                                        if self.unique_benchmark is None or 'mrbench' == self.unique_benchmark:
                                            # mrbench
                                            cmd = meta_cmd + ["--benchmark mrbench"]
                                            self.append_to_file(msg=' '.join(cmd))
                                        if self.unique_benchmark is None or 'terasort' == self.unique_benchmark:
                                            # terasort
                                            cmd = meta_cmd + ["--benchmark terasort"]
                                        self.append_to_file(msg=' '.join(cmd))
                                elif sys_name == 'kafka':
                                    if self.unique_benchmark is None or 'perf_test' == self.unique_benchmark:
                                        # perf_test
                                        cmd = meta_cmd + ["--benchmark perf_test"]
                                        self.append_to_file(msg=' '.join(cmd))
                                    if self.unique_benchmark is None or 'openmsg' == self.unique_benchmark:
                                        # openmsg
                                        for driver in self.benchmark_dict['kafka']['openmsg']['driver']:
                                            for workload in self.benchmark_dict['kafka']['openmsg']['workload']:
                                                cmd = meta_cmd + [
                                                    f"--benchmark openmsg",
                                                    f"--openmsg_driver {driver}",
                                                    f"--openmsg_workload {workload}"
                                                ]
                                                self.append_to_file(msg=' '.join(cmd))
                            if duration == -1:
                                print("We dont care about different severities for duration=-1")
                                break
        with open(self.output_file, 'r') as file:
            content = file.read()
        content = content.replace('REPLACE_WITH_TOTAL_NUM', f"{self.counter}")
        with open(self.output_file, 'w') as file:
            file.write(content)
    
    # def info(self,
    #          msg_ : str,
    #          rela = None,
    #          if_time = True):
    #     time_info = ""
    #     cur_ts = int(time.time()*1e9)
    #     if rela is None:
    #         time_info = f"[{str(cur_ts)}, {datetime.datetime.now().strftime('%H:%M:%S')}] "
    #     else:
    #         time_info = f"[{str(cur_ts)}, {datetime.datetime.now().strftime('%H:%M:%S')}, {round((cur_ts-rela)/1e9/60, 3)}min] "
    #     if if_time:
    #         print('\033[92m' + time_info + msg_ + '\033[0m')
    #         msg_ = time_info + msg_
    #     else:
    #         print('\033[92m' + msg_ + '\033[0m')
    #     with open(self.meta_log_loc, 'a') as fp:
    #         fp.write("%s\n" % msg_)
    
    # def create_dir_if_not_exist(self, path_):
    #     is_exsit = os.path.exists(path_)
    #     if not is_exsit:
    #         os.makedirs(path_)
    #     else:
    #         print(f'Directory {path_} already exists!')
    
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
parser = argparse.ArgumentParser(description="TEST \o/")
parser.add_argument('--sys_name', type = str, required=True,
            choices=['cassandra', 'hbase', 'hadoop', 'etcd', 'crdb', 'kafka', 'all'],
            help='Name of the distributed systems to be tested.')
parser.add_argument('--data_dir', type = str, required=True,    
            help='Name of data directory to store all the logs')
parser.add_argument('--start_time', type = int, required=True,
                    nargs='+', help='(A list of) start_time. Separated by space. For example: --start_time 10 20 30')
parser.add_argument('--duration', type = int, required=True,
                    nargs='+', help='(A list of) duration. Separated by space. For example: --start_time 10 20 30')
parser.add_argument('--fault_type', type = str, required=True,
                    nargs='+', choices=['nw','fs'],
                    help='(A list of) Types of slow faults to be injected.')
parser.add_argument('--bench_exec_time', type = str, required=False, default = '150',
                    help='Benchmark execution time. Default: 150s')
parser.add_argument('--severity', type = str, required=False, default = None,
                    choices=['nw', 'fs', 'nw-flaky', 'nw-slow'],
                    help='Run specific severity. For example: --severity slow-low')
parser.add_argument('--iter', type = int, required=False, default = 1,
                    help='Number of iterations. Default: 1')
parser.add_argument('--unique_benchmark', type = str, required=False, default = None,
                    help='Only run a specified benchmark. For example: --unique_benchmark ycsb')
parser.add_argument('--disable_port_check', action='store_true', default=False,
                    help='Disable port check')
parser.add_argument('--if_restart', action='store_true', default=False,
                    help='Disable port check')
parser.add_argument('--version', "-v", type = str, required=False, default = None)
parser.add_argument('--coverage', action='store_true', default=False)

args = parser.parse_args()
print(args.start_time)
print(args.duration)
t = GenerateTestScript(sys_name = args.sys_name,
            data_dir = args.data_dir,
            start_time_ary = args.start_time,
            duration_ary = args.duration,
            fault_type_ary = args.fault_type,
            exec_time = args.bench_exec_time,
            unique_benchmark = args.unique_benchmark,
            disable_port_check = args.disable_port_check,
            if_restart = args.if_restart,
            severity = args.severity,
            iter = args.iter,
            version = args.version,
            coverage_enabled = args.coverage,)
t.generate()
