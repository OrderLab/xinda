from xinda.systems.TestSystem import *

class Etcd(TestSystem):
    def test(self):
        # init
        self.info(self.fault.get_info(), if_time=False)
        if self.fault.type == 'nw':
            self.docker_up()
            time.sleep(10)
            self.docker_get_status()
            self.blockade_up()
        elif self.fault.type == 'fs':
            self.charybdefs_up()
            self.docker_up()
            time.sleep(10)
            self.docker_get_status()
        elif self.fault.type == 'none':
            self.docker_up()
            time.sleep(10)
            self.docker_get_status()
        else:
            raise ValueError(f"Fault type:{self.fault.type} is not one of {{nw, fs}}")
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
    
    def _load_ycsb(self):
        cmd = [self.tool.go_ycsb_bin,
               'load', 'etcd',
            #    '-P', os.path.join(self.tool.go_ycsb, ('workloads/workload' + self.benchmark.workload)),
               '-P', os.path.join(self.tool.go_ycsb_wkl, ('workload' + self.benchmark.workload)),
               '-p', f'recordcount={self.benchmark.recordcount}',
               '-p', f"etcd.endpoints=http://{self.container_info['etcd0']}:2379",
               '-p', f'threadcount={self.benchmark.threadcount}'
        ]
        cmd = [str(item) for item in cmd]
        p = subprocess.run(cmd)
        self.info(f"{self.tool.go_ycsb}/workloads/workload{self.benchmark.workload} successfully loaded")
    
    def _run_ycsb(self):
        cmd = [self.tool.go_ycsb_bin,
               'run', 'etcd',
            #    '-P', os.path.join(self.tool.go_ycsb, ('workloads/workload' + self.benchmark.workload)),
               '-P', os.path.join(self.tool.go_ycsb_wkl, ('workload' + self.benchmark.workload)),
               '-p', f'operationcount={self.benchmark.operationcount}',
               '-p', f"etcd.endpoints=http://{self.container_info['etcd0']}:2379",
               '--interval', self.benchmark.status_interval,
               '-p', f'threadcount={self.benchmark.threadcount}'
        ]
        cmd = [str(item) for item in cmd]
        # We don't have as summary in etcd.ycsb
        self.ycsb_process = subprocess.Popen(cmd, stdout=open(self.log.runtime,"w"), stderr=subprocess.DEVNULL)#, stderr=open(self.log.raw,"w"))
        # self.ycsb_process = subprocess.Popen(cmd, stderr=open(self.log.runtime, "w"), stdout=open(self.log.raw,"w"))
        self.start_time = int(time.time()*1e9)
        self.info("Benchmark:ycsb starts. We should inject faults after 30s till the cluster performance is stable", rela=self.start_time)
        # self.info("Benchmark:ycsb starts. Now wait 30s before cluster performance is stable", rela=self.start_time)
        # time.sleep(30)
    
    def _wait_till_benchmark_ends(self):
        cur_time = self.get_current_ts()
        if cur_time < int(self.benchmark.exec_time):
            delta_time = int(self.benchmark.exec_time) - cur_time
            self.info(f"Sleep {delta_time}s till benchmark ends")
            time.sleep(delta_time)
        self.ycsb_process.terminate()
        time.sleep(5)
        self.info("Benchmark safely ends", rela=self.start_time)
    
    def _post_process(self):
        p = subprocess.run(['docker-compose', 'logs'], stdout=open(self.log.compose,'w'), stderr =subprocess.STDOUT, cwd=self.tool.compose)




# nw_fault = SlowFault(
#     type_="nw", # nw or fs
#     location_ = "etcd0", # e.g., datanode
#     duration_ = 10,
#     severity_ = "slow3",
#     start_time_ = 35)
# fs_fault = SlowFault(
#     type_="fs", # nw or fs
#     location_ = "etcd0", # e.g., datanode
#     duration_ = 10,
#     severity_ = "100000",
#     start_time_ = 35)
# b = YCSB_ETCD(exec_time_='150',workload_='a', threadcount_=500)

# t = Etcd(sys_name_= "etcd",
#                fault_ = nw_fault,
#                benchmark_= b,
#                data_dir_= "xixi1")