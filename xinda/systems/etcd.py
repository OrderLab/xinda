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
        if self.benchmark.benchmark == 'ycsb':
            # load and run benchmark
            self._load_ycsb()
            self._run_ycsb()
            # inject slow faults
            if self.fault.type != 'none':
                self.inject()
            else:
                self.info("Fault type == none, no faults shall be injected")
            # wrap-up and end
            self._wait_till_ycsb_ends()
            self._post_process()
        elif self.benchmark.benchmark == 'etcd-official':
            self.run_official()
            # inject slow faults
            if self.fault.type != 'none':
                self.inject()
            else:
                self.info("Fault type == none, no faults shall be injected")
            # wrap-up and end
            self._wait_till_official_ends()
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
    
    def run_official(self):
        cmd = f'docker exec -it etcd-benchmark benchmark {self.benchmark.workload} --endpoints={self.benchmark.official_endpoints} {self.benchmark.official_flags}'
        self.official_process = subprocess.Popen(cmd, stdout=open(self.log.runtime,"w"), stderr=subprocess.DEVNULL, shell=True)
        self.start_time = int(time.time()*1e9)
        self.info(f"Benchmark:{self.benchmark.identifier} starts. We should inject faults after 30s till the cluster performance is stable", rela=self.start_time)
    
    def _wait_till_official_ends(self):
        # cur_time = self.get_current_ts()
        # if cur_time < int(self.benchmark.max_execution_time): # and self.official_process.poll() is not None:
        #     self.info(f"Waiting till benchmark ends. Current time:{cur_time}, max_execution_time:{self.benchmark.max_execution_time} {self.official_process.returncode}", rela=self.start_time)
        #     time.sleep(1)
        #     cur_time = self.get_current_ts()
        # # self.official_process.terminate()
        cur_time = self.get_current_ts()
        self.info(f"Waiting till benchmark ends. Current time:{cur_time}, max_execution_time:{self.benchmark.max_execution_time}", rela=self.start_time)
        self.official_process.communicate(timeout=self.benchmark.max_execution_time)
        if self.official_process.returncode == 0:
            self.info("Benchmark safely ends", rela=self.start_time)
        else:
            self.info(f"[FATAL ERROR] Benchmark returncode={self.official_process.returncode} (not zero)!", rela=self.start_time)
    
    def _wait_till_ycsb_ends(self):
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
#     duration_ = -1,
#     severity_ = "slow3",
#     start_time_ = 35)
# # fs_fault = SlowFault(
# #     type_="fs", # nw or fs
# #     location_ = "etcd0", # e.g., datanode
# #     duration_ = 10,
# #     severity_ = "100000",
# #     start_time_ = 35)
# # b = YCSB_ETCD(exec_time_='150',workload_='a', threadcount_=500)
# b = OFFICIAL_ETCD(workload_='lease-keepalive', total_=100000)

# import os
# t = Etcd(sys_name_= "etcd",
#                fault_ = nw_fault,
#                benchmark_= b,
#                data_dir_= "xixi1",
#                log_root_dir_ = f"{os.path.expanduser('~')}/workdir/data/default",
#                xinda_software_dir_ = f"{os.path.expanduser('~')}/workdir/xinda-software",
#                 xinda_tools_dir_ = f"{os.path.expanduser('~')}/workdir/xinda/tools",
#                 charybdefs_mount_dir_ = f"{os.path.expanduser('~')}/workdir/tmp")