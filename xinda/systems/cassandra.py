from xinda.systems.TestSystem import *

class Cassandra(TestSystem):
    def test(self):
        # init
        self.info(self.fault.get_info(), if_time=False)
        if self.fault.type == 'nw':
            self.docker_up()
            self._docker_status_checker()
            time.sleep(10)
            self.blockade_up()
        elif self.fault.type == 'fs':
            self.charybdefs_up()
            self.docker_up()
            self._docker_status_checker()
        elif self.fault.type == 'none':
            self.docker_up()
            self._docker_status_checker()
        else:
            raise ValueError(f"Fault type:{self.fault.type} is not one of {{nw, fs, none}}")
        self._init_cql()
        # load and run benchmark
        self._load_ycsb()
        self._run_ycsb()
        # inject slow faults
        if self.fault.type != 'none':
            self.inject()
        else:
            self.info("Fault type == none, no faults shall be injected")
        # wrap-up and end
        self._wait_till_benchmark_ends()
        self._post_process()
        self.docker_down()
        if self.fault.type == 'nw':
            self.blockade_down()
        elif self.fault.type == 'fs':
            self.charybdefs_down()
        self.info("THE END")
        
    def _docker_status_checker(self):
        cmd = ["docker exec -it cas1 nodetool status | grep 'UN ' | awk '{print $2}' | wc -l"]
        while True:
            num_normal_node = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout.strip()
            if num_normal_node == b'3':
                self.info("Cassandra cluster properly set up.")
                break
            else:
                print("Still waiting for cluster to set up. Sleep 10s")
                time.sleep(10)
        self.docker_get_status()
    
    def _init_cql(self):
        cmd = [self.tool.cas_cqlsh,
               self.container_info['cas1'],
               9042,
               '-f',
               self.tool.cas_init_cql
        ]
        cmd = [str(item) for item in cmd]
        p = subprocess.run(cmd)
        self.info("KEYSPACE:ycsb and TABLE:usertable initiated")
    
    def _load_ycsb(self):
        cmd = [os.path.join(self.tool.ycsb, 'bin/ycsb.sh'),
               'load', 'cassandra-cql',
               f"-p hosts={self.container_info['cas1']}",
               '-s',
            #    '-P', os.path.join(self.tool.ycsb, ('workloads/workload' + self.benchmark.workload)),
               '-P', os.path.join(self.tool.ycsb_wkl, ('workload' + self.benchmark.workload)),
               f'-p recordcount={self.benchmark.recordcount}'
        ]
        cmd = [str(item) for item in cmd]
        p = subprocess.run(cmd)
        self.info(f"{self.tool.ycsb}/workloads/workload{self.benchmark.workload} successfully loaded")
    
    def _run_ycsb(self):
        cmd = [os.path.join(self.tool.ycsb, 'bin/ycsb.sh'),
               'run', 'cassandra-cql',
               f"-p hosts={self.container_info['cas1']}",
               '-s',
            #    '-P', os.path.join(self.tool.ycsb, ('workloads/workload' + self.benchmark.workload)),
               '-P', os.path.join(self.tool.ycsb_wkl, ('workload' + self.benchmark.workload)),
               f'-p measurementtype={self.benchmark.measurementtype}',
               f'-p operationcount={self.benchmark.operationcount}',
               f'-p maxexecutiontime={self.benchmark.exec_time}',
               f'-p status.interval={self.benchmark.status_interval}'
        ]
        cmd = [str(item) for item in cmd]
        self.ycsb_process = subprocess.Popen(cmd, stderr=open(self.log.runtime, "w"), stdout=open(self.log.raw,"w"))
        self.start_time = int(time.time()*1e9)
        self.info("Benchmark:ycsb starts. We should inject faults after 30s till the cluster performance is stable", rela=self.start_time)
        # self.info("Benchmark:ycsb starts. Now wait 30s before cluster performance is stable", rela=self.start_time)
        # time.sleep(30)
    
    def _wait_till_benchmark_ends(self):
        self.ycsb_process.wait()
        self.info("Benchmark safely ends", rela=self.start_time)
    
    def _post_process(self):
        p = subprocess.run(['docker-compose', 'logs'], stdout=open(self.log.compose,'w'), stderr =subprocess.STDOUT, cwd=self.tool.compose)
        # Convert raw.log => ts.log
        cmd = f"cat {self.log.raw} | grep -e \"READ,\" -e \"UPDATE,\" -e \"SCAN,\" -e \"INSERT,\" -e \"READ-MODIFY-WRITE,\" > {self.log.time_series}"
        p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Convert raw.log => sum.log
        cmd = f"cat {self.log.raw} | grep -v -e \"READ,\" -e \"UPDATE,\" -e \"SCAN,\" -e \"INSERT,\" -e \"READ-MODIFY-WRITE,\" > {self.log.summary}"
        p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.info("Convert raw to ts/sum")


# nw_fault = SlowFault(
#     type_="nw", # nw or fs
#     location_ = "cas1", # e.g., datanode
#     duration_ = 30,
#     severity_ = "slow3",
#     start_time_ = 35)
# fs_fault = SlowFault(
#     type_="fs", # nw or fs
#     location_ = "cas1", # e.g., datanode
#     duration_ = 30,
#     severity_ = "100000",
#     start_time_ = 35)

# b = YCSB_CASSANDRA(exec_time_='150',workload_='a')

# t = Cassandra(sys_name_= "cassandra",
#                fault_ = nw_fault,
#                benchmark_= b,
#                data_dir_= "xixi1")

# t.docker_up()
# # sleep
# t.docker_status_checker()
# t.blockade_up()
# t.init_ycsb()
# t.load_ycsb()
# t.run_ycsb()
# # charybdefs start
# # benchmark start
# # inject slow faults
# t.docker_down()
# t.blockade_down()
# # charybdefs end
