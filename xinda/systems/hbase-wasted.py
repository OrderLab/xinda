import os
import subprocess
from Logging import Logging
from SlowFault import SlowFault
from Tool import Tool
import datetime
import time
import yaml
import docker # pip3 install docker
from TestSystem import TestSystem
from Benchmark import *
import threading

class HBase(TestSystem):
    def test(self):
        # init
        self.dest = 'hbase-regionserver2'
        self.info(self.fault.get_info(), if_time=False)
        if self.fault.type == 'nw':
            self.docker_up()
            time.sleep(60)
            self.info("A new cluster is properly set up.")
            self.docker_get_status()
            self.blockade_up()
        elif self.fault.type == 'fs':
            self.charybdefs_up()
            self.docker_up()
            time.sleep(60)
            self.info("A new cluster is properly set up.")
            self.docker_get_status()
        else:
            raise ValueError(f"Fault type:{self.fault.type} is not one of {{nw, fs}}")
        self._copy_file_to_container()
        self._init_hbase()
        # inject slow faults (in a background thread)
        self.start_time = int(time.time()*1e9)
        self.inject()
        # load-run the benchmark in cycles
        for iter in range(self.benchmark.num_cycle):
            self._load_ycsb(iter)
            self._run_ycsb(iter)
        # wrap-up and end
        self.inject_thread.join()
        # self._wait_till_benchmark_ends()
        self._post_process()
        self.docker_down()
        if self.fault.type == 'nw':
            self.blockade_down()
        else:
            self.charybdefs_down()
        self.info("THE END")
    
    def _copy_file_to_container(self):
        cmd = ['docker',
               'cp',
               self.tool.hbase_init,
               f"{self.dest}:/tmp/hbase-init.sh"]
        p = subprocess.run(cmd)
        cmd = ['docker',
               'cp',
               self.tool.hbase_check_pid,
               f"{self.dest}:/tmp/hbase-check-pid.sh"]
        p = subprocess.run(cmd)
        cmd = ['docker',
               'cp',
               self.tool.ycsb,
               f"{self.dest}:/tmp/"]
        p = subprocess.run(cmd)
    
    def _init_hbase(self):
        cmd = ['docker',
               'exec', '-it',
               self.dest,
               'bash', '/tmp/hbase-init.sh']
        p = subprocess.run(cmd)
        self.info("TABLE:usertable COLUMNFAMILY:family initiated")
    
    def inject(self):
        self.inject_thread = threading.Thread(target=super().inject)
        self.inject_thread.start()
    
    def _load_ycsb(self, iter):
        cmd = ['docker exec -it',
               self.dest,
               'sh -c',
               f'\"{self.tool.hbase_ycsb}/bin/ycsb load hbase12',
               '-s',
               f"-P {self.tool.hbase_ycsb}/workloads/workload{self.benchmark.workload}",
               '-cp /etc/hbase',
               f"-p measurementtype={self.benchmark.measurementtype}",
               f'-p recordcount={self.benchmark.recordcount}',
               f"-p maxexecutiontime={self.benchmark.load_exec_time}",
               f"-p status.interval={self.benchmark.status_interval}",
               f'-p columnfamily={self.benchmark.columnfamily}',
               f"> {self.log.raw_load_container[iter]}",
               f"2> {self.log.runtime_load_container[iter]}\""]
        cmd = ' '.join(cmd)
        self.info(f"[load-{iter}, loading] {self.dest}:{self.tool.hbase_ycsb}/workloads/workload{self.benchmark.workload}", rela=self.start_time)
        p = subprocess.run(cmd, shell=True)
        self.info(f"[load-{iter}, finished] {self.dest}:{self.tool.hbase_ycsb}/workloads/workload{self.benchmark.workload}", rela=self.start_time)
        # self.info(f"{self.dest}:{self.tool.hbase_ycsb}/workloads/workload{self.benchmark.workload} successfully loaded")
    
    def _run_ycsb(self, iter):
        cmd = ['docker exec -it',
               self.dest,
               'sh -c',
               f"\"{self.tool.hbase_ycsb}/bin/ycsb run hbase12",
               '-s',
               f"-P {self.tool.hbase_ycsb}/workloads/workload{self.benchmark.workload}",
               '-cp /etc/hbase',
               f"-p measurementtype={self.benchmark.measurementtype}",
               f"-p operationcount={self.benchmark.operationcount}",
               f"-p maxexecutiontime={self.benchmark.run_exec_time}",
               f"-p status.interval={self.benchmark.status_interval}",
               f"-p columnfamily={self.benchmark.columnfamily}",
               f"> {self.log.raw_run_container[iter]}",
               f"2> {self.log.runtime_run_container[iter]}\""]
        cmd = ' '.join(cmd)
        self.info(f"[run-{iter}, running] {self.dest}:{self.tool.hbase_ycsb}/workloads/workload{self.benchmark.workload}", rela=self.start_time)
        self.ycsb_process = subprocess.run(cmd, shell=True)
        self.info(f"[run-{iter}, finished] {self.dest}:{self.tool.hbase_ycsb}/workloads/workload{self.benchmark.workload}", rela=self.start_time)
        self.info("Benchmark:ycsb starts. We should inject faults after 30s till the cluster performance is stable", rela=self.start_time)
        # time.sleep(30)
    
    def _wait_till_benchmark_ends(self):
        cmd = ['docker exec -it',
               self.dest,
               'bash /tmp/hbase-check-pid.sh']
        cmd = ' '.join(cmd)
        p = subprocess.run(cmd, shell=True)
        self.info("Benchmark safely ends", rela=self.start_time)
    
    def _post_process(self):
        p = subprocess.run(['docker-compose', 'logs'], stdout=open(self.log.compose,'w'), stderr =subprocess.STDOUT, cwd=self.tool.compose)
        for iter in range(self.benchmark.num_cycle):
            # Copy logs to local
            cmd = f"docker cp {self.dest}:{self.log.raw_load_container[iter]} ."
            p = subprocess.run(cmd, cwd=self.log.data_dir, shell=True)
            cmd = f"docker cp {self.dest}:{self.log.runtime_load_container[iter]} ."
            p = subprocess.run(cmd, cwd=self.log.data_dir, shell=True)
            cmd = f"docker cp {self.dest}:{self.log.raw_run_container[iter]} ."
            p = subprocess.run(cmd, cwd=self.log.data_dir, shell=True)
            cmd = f"docker cp {self.dest}:{self.log.runtime_run_container[iter]} ."
            p = subprocess.run(cmd, cwd=self.log.data_dir, shell=True)
    
            # Convert raw.log => ts.log
            cmd = f"cat {self.log.raw_load[iter]} | grep -e \"READ,\" -e \"UPDATE,\" -e \"SCAN,\" -e \"INSERT,\" -e \"READ-MODIFY-WRITE,\" > {self.log.ts_load[iter]}"
            p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            cmd = f"cat {self.log.raw_run[iter]} | grep -e \"READ,\" -e \"UPDATE,\" -e \"SCAN,\" -e \"INSERT,\" -e \"READ-MODIFY-WRITE,\" > {self.log.ts_run[iter]}"
            p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Convert raw.log => sum.log
            cmd = f"cat {self.log.raw_load[iter]} | grep -v -e \"READ,\" -e \"UPDATE,\" -e \"SCAN,\" -e \"INSERT,\" -e \"READ-MODIFY-WRITE,\" > {self.log.sum_load[iter]}"
            cmd = f"cat {self.log.raw_run[iter]} | grep -v -e \"READ,\" -e \"UPDATE,\" -e \"SCAN,\" -e \"INSERT,\" -e \"READ-MODIFY-WRITE,\" > {self.log.sum_run[iter]}"
            p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.info("Convert raw to ts/sum")

nw_fault = SlowFault(
    type_="nw", # nw or fs
    location_ = "hbase-master", 
    duration_ = 30,
    severity_ = "slow3",
    start_time_ = 35)
fs_fault = SlowFault(
    type_="nw", # nw or fs
    location_ = "datanode", # e.g., datanode
    duration_ = 30,
    severity_ = "10000",
    start_time_ = 35)
b = YCSB_HBASE(run_exec_time_='20',
               load_exec_time_='10',
               workload_='a', 
               recordcount_='1000000',
               num_cycle_=2)

t = HBase(sys_name_= "hbase",
               fault_ = nw_fault,
               benchmark_= b,
               data_dir_= "xixi1")