# cassandra + nw
# python3 main.py --sys_name cassandra \
#                 --data_dir nw_test \
#                 --fault_type nw \
#                 --fault_location cas1 \
#                 --fault_duration 15 \
#                 --fault_severity slow3 \
#                 --fault_start_time 5 \
#                 --bench_exec_time 60

# cassandra + fs [PASSED]
# python3 main.py --sys_name cassandra \
#                 --data_dir fs_test \
#                 --fault_type fs \
#                 --fault_location cas1 \
#                 --fault_duration 15 \
#                 --fault_severity 10000 \
#                 --fault_start_time 5 \
#                 --bench_exec_time 60

# # hbase + nw
# python3 main.py --sys_name hbase \
#                 --data_dir nw_test \
#                 --fault_type nw \
#                 --fault_location datanode \
#                 --fault_duration 15 \
#                 --fault_severity slow3 \
#                 --fault_start_time 5 \
#                 --bench_exec_time 60

# # hbase + fs
# python3 main.py --sys_name hbase \
#                 --data_dir fs_test \
#                 --fault_type fs \
#                 --fault_location datanode \
#                 --fault_duration 15 \
#                 --fault_severity 10000 \
#                 --fault_start_time 5 \
#                 --bench_exec_time 60

# # hbase + none
# python3 main.py --sys_name hbase \
#                 --data_dir none_test \
#                 --fault_type none \
#                 --fault_location datanode \
#                 --fault_duration 15 \
#                 --fault_severity 10000 \
#                 --fault_start_time 5 \
#                 --bench_exec_time 60

import subprocess
import time, datetime
import argparse
def info(msg_ : str,
         rela = None,
         if_time = True):
    time_info = ""
    cur_ts = int(time.time()*1e9)
    if rela is None:
        time_info = f"[{str(cur_ts)}, {datetime.datetime.now().strftime('%H:%M:%S')}] "
    else:
        time_info = f"[{str(cur_ts)}, {datetime.datetime.now().strftime('%H:%M:%S')}, {round((cur_ts-rela)/1e9, 3)}] "
    if if_time:
        return(time_info + msg_ )
    else:
        return(msg_)

parser = argparse.ArgumentParser(description="Simple test")
parser.add_argument('--test_fault_types', action='store_true',
                    help='Test different fault types: fs, nw, and none')
parser.add_argument('--test_duration_minus_1', action='store_true',
                    help='Test if we set fault duration as -1')

args = parser.parse_args()
if args.test_fault_types is None and args.test_duration_minus_1 is None:
    print("Specify test flags")
    exit(1)
test_configs = {
    "kafka": "kafka1",
    "crdb": "roach1",
    "hadoop": "datanode",
    "hbase": "datanode",
    "etcd": "etcd0",
    "cassandra": "cas1",
}
benchmark_configs = {
    "hbase": ["ycsb"],
    "etcd": ["ycsb"],
    "cassandra": ["ycsb"],
    "crdb": ["ycsb"],#, "sysbench"],
    "hadoop": ["mrbench"],#,"terasort"],
    "kafka": ["openmsg","perf_test"],
    # "kafka": ['perf_test']
}

if args.test_fault_types:
    with open('./simple_test.log', 'a') as file:
        file.write(info("test_fault_types\n"))
    fault_configs = {
        # 'fs': '10000',
        'nw': 'slow-medium',
        # 'none': 'xxx' # random string
    }
    for sys in test_configs.keys():
        for type in fault_configs.keys():
            for benchmark in benchmark_configs[sys]:
                cmd = [f'python3 ../main.py --sys_name {sys}',
                            f'--data_dir {type}_test',
                            f'--fault_type {type}',
                            f'--fault_location {test_configs[sys]}',
                            '--fault_duration 15',
                            f'--fault_severity {fault_configs[type]}',
                            '--fault_start_time 5',
                            '--bench_exec_time 60',
                            f'--benchmark {benchmark}']
                cmd = ' '.join(cmd)
                with open('./simple_test.log', 'a') as file:
                    file.write(cmd+'\n')
                    file.write(info(f"[BEGIN] {sys} {type} \n"))
                try:
                    subprocess.run(cmd, shell=True)
                    with open('./simple_test.log', 'a') as file:
                        file.write(info(f"[End] {sys} {type} \n\n"))
                except:
                    exit(1)
if args.test_duration_minus_1:
    with open('./simple_test.log', 'a') as file:
        file.write(info("test_duration_minus_1\n"))
    for sys in test_configs.keys():
        # for type in ['fs', 'nw']:
        for type in ['nw']:
            for benchmark in benchmark_configs[sys]:
                cmd = [f'python3 ../main.py --sys_name {sys}',
                            f'--data_dir {type}_test',
                            f'--fault_type {type}',
                            f'--fault_location {test_configs[sys]}',
                            '--fault_duration -1',
                            f'--fault_severity abaaba',
                            '--fault_start_time 5',
                            '--bench_exec_time 60',
                            f'--benchmark {benchmark}']
                cmd = ' '.join(cmd)
                with open('./simple_test.log', 'a') as file:
                    file.write(cmd+'\n')
                    file.write(info(f"[BEGIN] {sys} {type} duration=-1\n"))
                try:
                    subprocess.run(cmd, shell=True)
                    with open('./simple_test.log', 'a') as file:
                        file.write(info(f"[End] {sys} {type} duration=-1\n\n"))
                except:
                    exit(1)