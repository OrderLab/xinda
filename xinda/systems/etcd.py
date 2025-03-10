from xinda.systems.TestSystem import *

class Etcd(TestSystem):
    def test(self):
        # init
        self.info(self.fault.get_info(), if_time=False)
        if self.fault.type == 'nw':
            self.docker_up()
            time.sleep(10)
            if self.cluster_size == 10:
                time.sleep(20)
            elif self.cluster_size == 20:
                time.sleep(40)
            self.docker_get_status()
            self.blockade_up()
        elif self.fault.type == 'fs':
            self.charybdefs_up()
            self.docker_up_charybdefs_etcd()
            time.sleep(10)
            if self.cluster_size == 10:
                time.sleep(20)
            elif self.cluster_size == 20:
                time.sleep(40)
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
        def get_container_info():
            client = docker.from_env()
            containers = client.containers.list(all=True)
            status = {}
            for container in containers:
                status[container.name] = container.status
            return status
        self.compose_file = 'docker-compose-all.yaml'
        if self.cluster_size == 10:
            self.compose_file = 'docker-compose-all-10node.yaml'
        elif self.cluster_size == 20:
            self.compose_file = 'docker-compose-all-20node.yaml'
        cmd = ['docker-compose',
                '-f', self.compose_file,
                'up',
                '-d']
        cmd = ' '.join(cmd)
        
        counter = 0
        while True:
            _ = subprocess.Popen(cmd, shell=True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, cwd=self.tool.compose)
            status = get_container_info()
            if len(status) == 0:
                time.sleep(1)
                continue
            if status[f'etcd{counter}'] != 'running':
                print(f"Sleep 1s for etcd{counter} to be running")
                time.sleep(1)
            else:
                counter += 1
                print(f"etcd{counter} is running")
            if counter == self.cluster_size:
                break
        self.info('Bringing up a new docker-compose cluster in the charybdefs way')
    
    def get_leader_name(self):
        self.endpoints = "etcd0:2379,etcd1:2379,etcd2:2379"
        if self.cluster_size == 10:
            self.endpoints = "etcd0:2379,etcd1:2379,etcd2:2379,etcd3:2379,etcd4:2379,etcd5:2379,etcd6:2379,etcd7:2379,etcd8:2379,etcd9:2379"
        elif self.cluster_size == 20:
            self.endpoints = "etcd0:2379,etcd1:2379,etcd2:2379,etcd3:2379,etcd4:2379,etcd5:2379,etcd6:2379,etcd7:2379,etcd8:2379,etcd9:2379,etcd10:2379,etcd11:2379,etcd12:2379,etcd13:2379,etcd14:2379,etcd15:2379,etcd16:2379,etcd17:2379,etcd18:2379,etcd19:2379"
        cmd = f'docker exec etcd0 etcdctl --write-out=table --endpoints={self.endpoints} endpoint status'
        awk_cmd = "awk '/true/ {print $2}'"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        cmd_output = p.stdout.read()
        self.info(cmd_output.decode('utf-8'))
        awk_process = subprocess.Popen(awk_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        leader_name, _ = awk_process.communicate(input=cmd_output)
        p.stdout.close()
        self.leader_name = leader_name.decode('utf-8').split(":")[0]
        etcd_nodes = ['etcd0','etcd1','etcd2']
        if self.cluster_size == 10:
            etcd_nodes = ['etcd0','etcd1','etcd2','etcd3','etcd4','etcd5','etcd6','etcd7','etcd8','etcd9']
        elif self.cluster_size == 20:
            etcd_nodes = ['etcd0','etcd1','etcd2','etcd3','etcd4','etcd5','etcd6','etcd7','etcd8','etcd9','etcd10','etcd11','etcd12','etcd13','etcd14','etcd15','etcd16','etcd17','etcd18','etcd19']
        if self.leader_name not in etcd_nodes:
            raise ValueError(f"Leader name {self.leader_name} is not in {etcd_nodes}")
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
        self.ycsb_endpoints = f"http://{self.container_info['etcd0']}:2379"
        if self.cluster_size == 10:
            self.ycsb_endpoints = f"http://{self.container_info['etcd0']}:2379,{self.container_info['etcd1']}:2379,{self.container_info['etcd2']}:2379,{self.container_info['etcd3']}:2379,{self.container_info['etcd4']}:2379,{self.container_info['etcd5']}:2379,{self.container_info['etcd6']}:2379,{self.container_info['etcd7']}:2379,{self.container_info['etcd8']}:2379,{self.container_info['etcd9']}:2379"
        elif self.cluster_size == 20:
            self.ycsb_endpoints = f"http://{self.container_info['etcd0']}:2379,{self.container_info['etcd1']}:2379,{self.container_info['etcd2']}:2379,{self.container_info['etcd3']}:2379,{self.container_info['etcd4']}:2379,{self.container_info['etcd5']}:2379,{self.container_info['etcd6']}:2379,{self.container_info['etcd7']}:2379,{self.container_info['etcd8']}:2379,{self.container_info['etcd9']}:2379,{self.container_info['etcd10']}:2379,{self.container_info['etcd11']}:2379,{self.container_info['etcd12']}:2379,{self.container_info['etcd13']}:2379,{self.container_info['etcd14']}:2379,{self.container_info['etcd15']}:2379,{self.container_info['etcd16']}:2379,{self.container_info['etcd17']}:2379,{self.container_info['etcd18']}:2379,{self.container_info['etcd19']}:2379"
        cmd = [self.tool.go_ycsb_bin,
               'load', 'etcd',
               '-P', os.path.join(self.tool.go_ycsb_wkl, ('workload' + self.benchmark.workload)),
               '-p', f'recordcount={self.benchmark.recordcount}',
               '-p', f"etcd.endpoints={self.ycsb_endpoints}",
               '-p', f'threadcount={self.benchmark.threadcount}'
        ]
        cmd = [str(item) for item in cmd]
        p = subprocess.run(cmd)
        self.info(f"{self.tool.go_ycsb}/workloads/workload{self.benchmark.workload} successfully loaded")
    
    def _run_ycsb(self):
        cmd = [self.tool.go_ycsb_bin,
               'run', 'etcd',
               '-P', os.path.join(self.tool.go_ycsb_wkl, ('workload' + self.benchmark.workload)),
               '-p', f'operationcount={self.benchmark.operationcount}',
               '-p', f"etcd.endpoints={self.ycsb_endpoints}",
               '--interval', self.benchmark.status_interval,
               '-p', f'threadcount={self.benchmark.threadcount}'
        ]
        cmd = [str(item) for item in cmd]
        self.ycsb_process = subprocess.Popen(cmd, stdout=open(self.log.runtime,"w"), stderr=subprocess.DEVNULL)#, stderr=open(self.log.raw,"w"))
        self.start_time = int(time.time()*1e9)
        self.info("Benchmark:ycsb starts. We should inject faults after 30s till the cluster performance is stable", rela=self.start_time)
    
    def _run_ycsb_double_wrapper(self):
        self.start_time = int(time.time()*1e9)
        double_run_thread = threading.Thread(target=self._run_ycsb_double)
        double_run_thread.start()
    
    def _run_ycsb_double(self):
        def _wait_till_process_ends(self, p, end_time):
            cur_time = self.get_current_ts()
            if cur_time < int(end_time):
                delta_time = int(end_time) - cur_time
                self.info(f"Sleep {delta_time}s till current benchmark ends")
                time.sleep(delta_time)
            p.terminate()
        
        wkl = 'readonly'
        cmd = [self.tool.go_ycsb_bin,
               'run', 'etcd',
               '-P', os.path.join(self.tool.go_ycsb_wkl, ('workload' + wkl)),
               '-p', f'operationcount={self.benchmark.operationcount}',
               '-p', f"etcd.endpoints=http://{self.container_info['etcd0']}:2379",
               '--interval', self.benchmark.status_interval,
               '-p', f'threadcount={self.benchmark.threadcount}'
        ]
        cmd = [str(item) for item in cmd]
        log1 = os.path.join(self.log.data_dir, 'runtime-' + self.log.description + f"-{wkl}.log")
        p1 = subprocess.Popen(cmd, stdout=open(log1,"w"), stderr=subprocess.DEVNULL)
        self.info(f"Benchmark:ycsb-{wkl} starts.", rela=self.start_time)
        _wait_till_process_ends(self, p=p1, end_time=90)
        
        wkl = 'writeonly'
        cmd = [self.tool.go_ycsb_bin,
               'run', 'etcd',
               '-P', os.path.join(self.tool.go_ycsb_wkl, ('workload' + wkl)),
               '-p', f'operationcount={self.benchmark.operationcount}',
               '-p', f"etcd.endpoints=http://{self.container_info['etcd0']}:2379",
               '--interval', self.benchmark.status_interval,
               '-p', f'threadcount={self.benchmark.threadcount}'
        ]
        cmd = [str(item) for item in cmd]
        log2 = os.path.join(self.log.data_dir, 'runtime-' + self.log.description + f"-{wkl}.log")
        self.ycsb_process = subprocess.Popen(cmd, stdout=open(log2,"w"), stderr=subprocess.DEVNULL)
        self.info(f"Benchmark:ycsb-{wkl} starts", rela=self.start_time)
    
    def run_official(self):
        cmd = f'docker exec -it etcd-benchmark benchmark {self.benchmark.workload} --endpoints={self.benchmark.official_endpoints} {self.benchmark.official_flags}'
        self.official_process = subprocess.Popen(cmd, stdout=open(self.log.runtime,"w"), stderr=subprocess.DEVNULL, shell=True)
        self.start_time = int(time.time()*1e9)
        self.info(f"Benchmark:{self.benchmark.identifier} starts. We should inject faults after 30s till the cluster performance is stable", rela=self.start_time)
    
    def _wait_till_official_ends(self):
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
        cmd = f'docker exec etcd0 etcdctl --write-out=table --endpoints={self.endpoints} endpoint status'
        awk_cmd = "awk '/true/ {print $2}'"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        cmd_output = p.stdout.read()
        self.info(cmd_output.decode('utf-8'))
        awk_process = subprocess.Popen(awk_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        cur_leader_name, _ = awk_process.communicate(input=cmd_output)
        p.stdout.close()
        cur_leader_name = cur_leader_name.decode('utf-8').strip()[:5]
        self.info(f"Current leader: {cur_leader_name}; Previous leader: {self.leader_name}; Leader changed: {cur_leader_name != self.leader_name}")