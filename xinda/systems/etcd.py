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
            self.docker_up_charybdefs_etcd()
            time.sleep(10)
            self.docker_get_status()
        elif self.fault.type == 'none':
            self.docker_up()
            time.sleep(10)
            self.docker_get_status()
        else:
            raise ValueError(f"Fault type:{self.fault.type} is not one of {{nw, fs}}")
        self.get_leader_name()
        if self.benchmark.benchmark == 'ycsb':
            # load and run benchmark
            self._load_ycsb()
            self._run_ycsb()
            # inject slow faults
            if self.fault.type != 'none':
                self.inject(cfs_pattern=f".*{self.fault.location}.*")
            else:
                self.info("Fault type == none, no faults shall be injected")
            # wrap-up and end
            self._wait_till_ycsb_ends()
        elif self.benchmark.benchmark == 'etcd-official':
            self.run_official()
            # inject slow faults
            if self.fault.type != 'none':
                self.inject(cfs_pattern=f".*{self.fault.location}.*")
            else:
                self.info("Fault type == none, no faults shall be injected")
            # wrap-up and end
            self._wait_till_official_ends()
        self._post_process()
        self.docker_down()
        if self.fault.type == 'nw':
            self.blockade_down()
        elif self.fault.type == 'fs':
            self.charybdefs_down()
            # Cleanning the compose process
            cmd = "ps aux | grep 'docker-compose' | grep -e 'T' -e 'S' | awk '{print $2}' | xargs kill -9"
            _ = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.info("THE END")
    
    def docker_up_charybdefs_etcd(self):
        cmd = ['docker-compose',
                '-f', f'docker-compose-all.yaml',
                'up',
                '-d']
        cmd = ' '.join(cmd)
        print("Try exactly 4 times :O")
        for i in range(4):
            _ = subprocess.Popen(cmd, shell=True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, cwd=self.tool.compose)
            time.sleep(1)
            print(f'try again {i+1}/4')
        self.info('Bringing up a new docker-compose cluster in the charybdefs way')
    
    def get_leader_name(self):
        cmd = 'docker exec etcd0 etcdctl --write-out=table --endpoints=etcd0:2379,etcd1:2379,etcd2:2379 endpoint status'
        awk_cmd = "awk '/true/ {print $2}'"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        cmd_output = p.stdout.read()
        self.info(cmd_output.decode('utf-8'))
        awk_process = subprocess.Popen(awk_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        leader_name, _ = awk_process.communicate(input=cmd_output)
        p.stdout.close()
        self.leader_name = leader_name.decode('utf-8').strip()[:5]
        etcd_nodes = ['etcd0','etcd1','etcd2']
        if self.leader_name not in etcd_nodes:
            raise ValueError(f"Leader name {self.leader_name} is not in {{etcd0, etcd1, etcd2}}")
        etcd_nodes.remove(self.leader_name)
        self.follower_name = etcd_nodes[0]
        self.info(f"Leader: {self.leader_name}, followers:{etcd_nodes}, choose one follower: {self.follower_name}")
        fault_loc = self.fault.location
        if self.fault.location == 'leader':
            self.fault.location = self.leader_name
        elif self.fault.location == 'follower':
            self.fault.location = self.follower_name
        self.info(f"Fault injection location changed from {fault_loc} to {self.fault.location}")
    
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
        cmd = 'docker exec etcd0 etcdctl --write-out=table --endpoints=etcd0:2379,etcd1:2379,etcd2:2379 endpoint status'
        awk_cmd = "awk '/true/ {print $2}'"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        cmd_output = p.stdout.read()
        self.info(cmd_output.decode('utf-8'))
        awk_process = subprocess.Popen(awk_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        cur_leader_name, _ = awk_process.communicate(input=cmd_output)
        p.stdout.close()
        cur_leader_name = cur_leader_name.decode('utf-8').strip()[:5]
        self.info(f"Current leader: {cur_leader_name}; Previous leader: {self.leader_name}; Leader changed: {cur_leader_name != self.leader_name}")




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

# python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir 11_11 --fault_type fs --fault_location leader --fault_duration 30 --fault_severity 10000 --fault_start_time 10 --bench_exec_time 60 --ycsb_wkl writeonly --benchmark ycsb

# python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir 11_11 --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-high --fault_start_time 10 --bench_exec_time 60 --ycsb_wkl writeonly --benchmark ycsb