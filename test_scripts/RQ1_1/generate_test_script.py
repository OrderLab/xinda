import os
import subprocess
import yaml
import time
import datetime
import argparse

class GenerateTestScript():
    def __init__(self,
                 sys_name,
                 data_dir,
                 start_time_ary,
                 duration_ary,
                 fault_type_ary):
        # self.output_file=f"{os.path.expanduser('~')}/xinda/test_scripts/RQ1_1/commands.txt"
        self.identifier = f"{sys_name}-{'-'.join(fault_type_ary)}-dur-{'-'.join([str(item) for item in duration_ary])}"
        self.output_file = self.identifier + ".sh"
        self.main_py=f"{os.path.expanduser('~')}/workdir/xinda/main.py"
        self.counter = 0
        # self.meta_log_loc=f"{os.path.expanduser('~')}/workdir/xinda/test_scripts/RQ1_1/meta.{datetime.datetime.now().strftime('%m.%d.%H.%M.%S')}.log"
        self.meta_log_loc=f"{os.path.expanduser('~')}/workdir/xinda/test_scripts/RQ1_1/meta-{self.identifier}.log"
        if sys_name == 'all':
            sys_name = ['crdb', 'cassandra', 'hbase', 'kafka', 'etcd', 'hadoop']
        else:
            sys_name = [sys_name]
        self.sys_name_ary = sys_name
        self.data_dir = data_dir
        self.start_time_ary = start_time_ary
        self.duration_ary = duration_ary
        self.fault_type_ary = fault_type_ary
        # location
        self.location_dict = {
            'cassandra': ['cas1', 'cas2'],
            'crdb': ['roach1', 'roach2'],
            'etcd': ['leader', 'follower'],
            'hadoop': ['datanode', 'namenode'],
            'hbase-fs': ['datanode', 'namenode'],
            'hbase-nw': ['datanode', 'namenode', 'hbase-master','hbase-regionserver'],
            'kafka': ['kafka1', 'kafka2']
        }
        # self.cassandra_location = ['cas1', 'cas2']
        # self.crdb_location = ['roach1', 'roach2']
        # self.etcd_location = ['etcd0', 'etcd1']
        # self.hadoop_location = ['datanode', 'namenode']
        # self.hbase_fs_location = ['datanode', 'namenode']
        # self.hbase_nw_location = ['datanode', 'namenode', 'hbase-master','hbase-regionserver']
        # self.kafka_location = ['kafka1', 'kafka2']
        # ycsb
        # self.ycsb_wkl = ['readonly', 'writeonly', 'mixed', 'b', 'd', 'e', 'f']
        # self.ycsb_wkl_crdb = ['a', 'b', 'c', 'd', 'e', 'f']
        self.ycsb_wkl = ['readonly', 'writeonly', 'mixed']
        self.ycsb_wkl_crdb = ['a', 'c']
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
            {'stm': ['--etcd_official_total 380000 --etcd_official_isolation r --etcd_official_locker stm',
                     '--etcd_official_total 130000 --etcd_official_isolation s --etcd_official_locker stm',
                     '--etcd_official_total 400000 --etcd_official_isolation c --etcd_official_locker stm',
                     '--etcd_official_total 130000 --etcd_official_isolation ss --etcd_official_locker stm',
                     '--etcd_official_total 6000 --etcd_official_isolation r --etcd_official_locker lock-client',
                     '--etcd_official_total 6000 --etcd_official_isolation s --etcd_official_locker lock-client',
                     '--etcd_official_total 6000 --etcd_official_isolation c --etcd_official_locker lock-client',
                     '--etcd_official_total 6000 --etcd_official_isolation ss --etcd_official_locker lock-client']},
            {'txn-put': ['--etcd_official_total 13000']},
            {'watch': ['--etcd_official_total 12000']},
            {'watch-get': ['--etcd_official_num_watchers 1000000']}
        ]
        # severity
        self.severity_dict = {
            'nw': ['slow-low', 'slow-medium', 'slow-high', 'flaky-low', 'flaky-medium', 'flaky-high'],
            'fs': [1000, 10000, 100000, 1000000]
        }
        # benchmark
        self.benchmark_dict = {
            "hbase": {"ycsb": self.ycsb_wkl},
            "etcd": {"ycsb": self.ycsb_wkl},
            "cassandra": {"ycsb": self.ycsb_wkl},
            "crdb": {
                "ycsb": self.ycsb_wkl_crdb,
                "sysbench": self.sysbench_wkl
                },
            "hadoop": {
                "mrbench": "mrbench",
                "terasort": "terasort"},
            "kafka": {
                "openmsg": {
                    "driver": ["kafka-latency", 
                               "kafka-throughput",
                               "kafka-exactly-once",
                               "kafka-big-batches-gzip",
                               "kafka-no-linger",
                               "kafka-sync"],
                    "workload": ["1-topic-1-partition-1kb",
                                 "1-topic-16-partitions-1kb",
                                 "1-topic-100-partitions-1kb"
                                 ]},
                "perf_test": "perf_test"
                }
        }
        # self.nw_severity = ['slow-low', 'slow-medium', 'slow-high', 'flaky-low', 'flaky-medium', 'flaky-high']
        # self.fs_severity = [1000, 10000, 100000, 1000000]
    
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
                                    f"--bench_exec_time 150"]
                                if sys_name in ['hbase', 'etcd', 'cassandra', 'crdb']:
                                    for wkl in self.benchmark_dict[sys_name]['ycsb']:
                                        cmd = meta_cmd + [
                                            f"--ycsb_wkl {wkl}",
                                            f"--benchmark ycsb"]
                                        self.append_to_file(msg=' '.join(cmd))
                                    if sys_name == 'crdb':
                                        # sysbench
                                        for lua_scheme in self.sysbench_wkl:
                                            cmd = meta_cmd + [
                                                f"--benchmark sysbench",
                                                f"--sysbench_lua_scheme {lua_scheme}"
                                            ]
                                            self.append_to_file(msg=' '.join(cmd))
                                    if sys_name == 'etcd':
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
                                    # mrbench
                                    cmd = meta_cmd + ["--benchmark mrbench"]
                                    self.append_to_file(msg=' '.join(cmd))
                                    # terasort
                                    cmd = meta_cmd + ["--benchmark terasort"]
                                    self.append_to_file(msg=' '.join(cmd))
                                elif sys_name == 'kafka':
                                    # perf_test
                                    cmd = meta_cmd + ["--benchmark perf_test"]
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
        if filename is None:
            filename = self.output_file
        self.counter = self.counter + 1
        begin_line = f"echo \"## [$(date +%s%N), $(date +\"%H:%M:%S\"), BEGIN] {self.counter} / REPLACE_WITH_TOTAL_NUM\" >> {self.meta_log_loc}"
        end_line = f"echo \"## [$(date +%s%N), $(date +\"%H:%M:%S\"), END] {self.counter} / REPLACE_WITH_TOTAL_NUM\" >> {self.meta_log_loc}"
        with open(filename, 'a') as fp:
            fp.write("%s\n" % begin_line)
            fp.write("%s\n" % msg)
            fp.write("%s\n\n" % end_line)

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
args = parser.parse_args()
print(args.start_time)
print(args.duration)
t = GenerateTestScript(sys_name = args.sys_name,
            data_dir = args.data_dir,
            start_time_ary = args.start_time,
            duration_ary = args.duration,
            fault_type_ary = args.fault_type)
t.generate()
