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
                 start_time1,
                 start_time2,
                 duration_ary,
                 fault_type_ary,
                 exec_time,
                 severity, 
                 concurrent,
                 iter):
        self.iter = iter
        self.identifier = f"{sys_name}-{'-'.join(fault_type_ary)}-dur-{'-'.join([str(item) for item in duration_ary])}-st-{start_time1}To{start_time2}-{iter}iter"
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
        self.start_time_ary = list(range(start_time1, start_time2+1))
        self.duration_ary = duration_ary
        self.fault_type_ary = fault_type_ary
        self.exec_time = exec_time
        self.concurrent = concurrent
        # location
        self.location_dict = {
            'copilot': ['replica1', 'replica2', 'replica3'],
            'epaxos': ['replica1'],
            'multipaxos': ['replica1', 'replica2'],
        }
        # start_time
        self.start_time_dict = {
            'copilot': self.start_time_ary,
            'epaxos': [start_time1],
            'multipaxos': [start_time1]
        }
        self.scheme_ary = ['multipaxos', 'epaxos', 'copilot']
        # severity
        self.severity_dict = {
            'nw': ['slow-100us', 'slow-1ms', 'slow-10ms', 'slow-100ms', 'slow-1s', 'flaky-p1', 'flaky-p10', 'flaky-p40', 'flaky-p70'],
            'fs': [1000, 10000, 100000, 1000000]
        }
        if severity is not None:
            if severity == 'nw':
                self.severity_dict = {'nw': self.severity_dict['nw']}
            elif severity == 'fs':
                self.severity_dict = {'fs': self.severity_dict['fs']}
            elif severity == 'nw-flaky':
                self.severity_dict = {'nw': ['flaky-p1','flaky-p10', 'flaky-p40', 'flaky-p70']}
            elif severity == 'nw-slow':
                self.severity_dict = {'nw': ['slow-100us', 'slow-1ms', 'slow-10ms', 'slow-100ms', 'slow-1s']}
        # benchmark
        self.benchmark = 'copilot'
    
    def generate(self):
        for sys_name in self.sys_name_ary:
            benchmark_ary = ['copilot']
            for scheme in self.scheme_ary:
                for conc in self.concurrent:
                    for duration in self.duration_ary:
                        for start_time in self.start_time_dict[scheme]:
                            for fault_type in self.fault_type_ary:
                                severity_ary = self.severity_dict[fault_type]
                                location_ary = self.location_dict[scheme]
                                for severity in severity_ary:
                                    for location in location_ary:
                                        meta_cmd = [f"python3 {self.main_py}",
                                            f"--sys_name {sys_name}",
                                            f"--data_dir copilot",
                                            f"--fault_type {fault_type}",
                                            f"--fault_location {location}",
                                            f"--fault_duration {duration}",
                                            f"--fault_severity {severity}",
                                            f"--fault_start_time {start_time}",
                                            f"--bench_exec_time {self.exec_time}",
                                            "--benchmark copilot",
                                            f"--copilot_concurrency {conc}",
                                            f"--copilot_scheme {scheme}"]
                                        # meta_cmd.append("xx")
                                        self.append_to_file(msg=' '.join(meta_cmd))
                                        if duration == -1:
                                            print("We dont care about different locations for duration=-1")
                                            break
                                    if duration == -1:
                                        print("We dont care about different severities for duration=-1")
                                        break
                                if duration == -1:
                                    print("We dont care about different fault types for duration=-1")
                                    break
                            if duration == -1:
                                print("We dont care about different fault durations for duration=-1")
                                break
        with open(self.output_file, 'r') as file:
            content = file.read()
        content = content.replace('REPLACE_WITH_TOTAL_NUM', f"{self.counter}")
        with open(self.output_file, 'w') as file:
            file.write(content)
    
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
            choices=['cassandra', 'hbase', 'hadoop', 'etcd', 'crdb', 'kafka', 'all', 'copilot'],
            help='Name of the distributed systems to be tested.')
parser.add_argument('--data_dir', type = str, required=True,    
            help='Name of data directory to store all the logs')
# parser.add_argument('--start_time', type = int, required=True,
#                     nargs='+', help='(A list of) start_time. Separated by space. For example: --start_time 10 20 30')
parser.add_argument('--start_time1', type = int, required=True)
parser.add_argument('--start_time2', type = int, required=True)
parser.add_argument('--duration', type = int, required=True,
                    nargs='+', help='(A list of) duration. Separated by space. For example: --duration 10 20 30')
parser.add_argument('--concurrent', type = int, required=True,
                    nargs='+', help='(A list of) duration. Separated by space. For example: --concurrent 1 10')
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

args = parser.parse_args()
print(list(range(args.start_time1, args.start_time2+1)))
print(args.duration)
t = GenerateTestScript(sys_name = args.sys_name,
            data_dir = args.data_dir,
            start_time1 = args.start_time1,
            start_time2 = args.start_time2,
            duration_ary = args.duration,
            fault_type_ary = args.fault_type,
            exec_time = args.bench_exec_time,
            severity = args.severity,
            concurrent = args.concurrent,
            iter = args.iter)
t.generate()
