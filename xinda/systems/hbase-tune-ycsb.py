from xinda.systems.TestSystem import *

class HBase(TestSystem):
    def test(self):
        # init
        self.dest = 'hbase-regionserver2'
        self.dest2 = 'hbase-regionserver'
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
        elif self.fault.type == 'none':
            self.docker_up()
            time.sleep(60)
            self.info("A new cluster is properly set up.")
            self.docker_get_status()
        else:
            raise ValueError(f"Fault type:{self.fault.type} is not one of {{nw, fs}}")
        self._copy_file_to_container()
        self._init_hbase()
        self._load_ycsb()
        self._load_ycsb2()
        self.start_time = int(time.time()*1e9)
        # inject slow faults (in a background thread)
        if self.fault.type != 'none':
            self.inject()
        else:
            self.info("Fault type == none, no faults shall be injected")
        self._run_ycsb2()
        self._run_ycsb()
        # wrap-up and end
        if self.fault.type != 'none':
            self.inject_thread.join()
        self._post_process()
        self.docker_down()
        if self.fault.type == 'nw':
            self.blockade_down()
        elif self.fault.type == 'fs':
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
        cmd = ['docker',
               'cp',
               self.tool.ycsb_wkl_root,
               f"{self.dest}:/tmp/"]
        p = subprocess.run(cmd)
        
        cmd = ['docker',
               'cp',
               self.tool.ycsb,
               f"{self.dest2}:/tmp/"]
        p = subprocess.run(cmd)
        cmd = ['docker',
               'cp',
               self.tool.ycsb_wkl_root,
               f"{self.dest2}:/tmp/"]
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
    
    def _load_ycsb(self):
        cmd = ['docker exec -it',
               self.dest,
               'sh -c',
               f'\"{self.tool.hbase_ycsb}/bin/ycsb load hbase20',
               '-s',
               f"-P {self.tool.hbase_ycsb_wkl}/workload{self.benchmark.workload}",
               '-cp /etc/hbase',
               f'-p recordcount={self.benchmark.recordcount}',
               '-p insertstart=0',
               '-p insertcount=5000',
               f"-p columnfamily={self.benchmark.columnfamily}\""]
        cmd = ' '.join(cmd)
        p = subprocess.run(cmd, shell=True)
        self.info(f"{self.tool.ycsb}/workloads/workload{self.benchmark.workload} successfully loaded")
    
    def _load_ycsb2(self):
        cmd = ['docker exec -it',
               self.dest2,
               'sh -c',
               f'\"{self.tool.hbase_ycsb}/bin/ycsb load hbase20',
               '-s',
               f"-P {self.tool.hbase_ycsb_wkl}/workload{self.benchmark.workload}",
               '-cp /etc/hbase',
               f'-p recordcount={self.benchmark.recordcount}',
               '-p insertstart=5000',
               '-p insertcount=5000',
               f"-p columnfamily={self.benchmark.columnfamily}\""]
        cmd = ' '.join(cmd)
        p = subprocess.run(cmd, shell=True)
        self.info(f"{self.tool.ycsb}/workloads/workload{self.benchmark.workload} family2 successfully loaded")
    
    def _run_ycsb(self):
        cmd = ['docker exec -it',
               self.dest,
               'sh -c',
               f"\"{self.tool.hbase_ycsb}/bin/ycsb run hbase20",
               '-s',
               f"-P {self.tool.hbase_ycsb_wkl}/workload{self.benchmark.workload}",
               '-cp /etc/hbase',
               f"-p measurementtype={self.benchmark.measurementtype}",
               f"-p operationcount={self.benchmark.operationcount}",
               f"-p maxexecutiontime={self.benchmark.exec_time}",
               f"-p status.interval={self.benchmark.status_interval}",
               f"-p columnfamily={self.benchmark.columnfamily}",
               f"-p threadcount=8",
               f"> {self.log.raw_container}",
               f"2> {self.log.runtime_container}\""]
        cmd = ' '.join(cmd)
        self.info("Benchmark:ycsb starts.", rela=self.start_time)
        self.ycsb_process = subprocess.run(cmd, shell=True)
    
    def _run_ycsb2(self):
        cmd = ['docker exec -it',
               self.dest2,
               'sh -c',
               f"\"{self.tool.hbase_ycsb}/bin/ycsb run hbase20",
               '-s',
               f"-P {self.tool.hbase_ycsb_wkl}/workload{self.benchmark.workload}",
               '-cp /etc/hbase',
               f"-p measurementtype={self.benchmark.measurementtype}",
               f"-p operationcount={self.benchmark.operationcount}",
               f"-p maxexecutiontime={self.benchmark.exec_time}",
               f"-p status.interval={self.benchmark.status_interval}",
               "-p columnfamily=family2",
               f"-p threadcount=8",
               f"> {self.log.raw_container}-{self.dest2}",
               f"2> {self.log.runtime_container}-{self.dest2}\""]
        cmd = ' '.join(cmd)
        self.info("Benchmark:ycsb2 starts (family2).", rela=self.start_time)
        self.ycsb_process2 = subprocess.Popen(cmd, shell=True)
    
    def _wait_till_benchmark_ends(self):
        cmd = ['docker exec -it',
               self.dest,
               'bash /tmp/hbase-check-pid.sh']
        cmd = ' '.join(cmd)
        self.info("Now wait until the benchmark ends", rela=self.start_time)
        p = subprocess.run(cmd, shell=True)
        self.info("Benchmark safely ends", rela=self.start_time)
    
    def _post_process(self):
        p = subprocess.run(['docker-compose', 'logs'], stdout=open(self.log.compose,'w'), stderr =subprocess.STDOUT, cwd=self.tool.compose)
        cmd = f"docker cp {self.dest}:{self.log.raw_container} ."
        p = subprocess.run(cmd, cwd=self.log.data_dir, shell=True)
        cmd = f"docker cp {self.dest}:{self.log.runtime_container} ."
        p = subprocess.run(cmd, cwd=self.log.data_dir, shell=True)
        # Convert raw.log => ts.log
        cmd = f"cat {self.log.raw} | grep -e \"READ,\" -e \"UPDATE,\" -e \"SCAN,\" -e \"INSERT,\" -e \"READ-MODIFY-WRITE,\" > {self.log.time_series}"
        p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Convert raw.log => sum.log
        cmd = f"cat {self.log.raw} | grep -v -e \"READ,\" -e \"UPDATE,\" -e \"SCAN,\" -e \"INSERT,\" -e \"READ-MODIFY-WRITE,\" > {self.log.summary}"
        p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        cmd = f"docker cp {self.dest2}:{self.log.raw_container}-{self.dest2} ."
        p = subprocess.run(cmd, cwd=self.log.data_dir, shell=True)
        cmd = f"docker cp {self.dest2}:{self.log.runtime_container}-{self.dest2} ."
        p = subprocess.run(cmd, cwd=self.log.data_dir, shell=True)
        self.info("Convert raw to ts/sum")