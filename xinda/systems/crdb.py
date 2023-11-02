from xinda.systems.TestSystem import *

class Crdb(TestSystem):
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
            raise ValueError(f"Fault type:{self.fault.type} is not one of {{nw, fs, none}}")
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
    
    def docker_up(self):
        super().docker_up()
        time.sleep(20)
        cmd = 'docker exec -it roach0 ./cockroach --host=roach1:26357 init --insecure'
        _ = subprocess.run(cmd, shell=True)
    
    def _load_ycsb(self):
        cmd = ['docker exec -it roach0',
               './cockroach workload init ycsb',
               '--drop',
               self.benchmark.load_connection_string]
        cmd = ' '.join(cmd)
        p = subprocess.run(cmd, shell=True)
        self.info("./cockroach YCSB workload successfully loaded")
    
    def _run_ycsb(self):
        cmd = ['docker exec -it roach0',
               './cockroach workload run ycsb',
               self.benchmark.run_connection_string,
               f'--workload={self.benchmark.workload}',
               f'--max-ops={self.benchmark.operationcount}',
               f'--duration={self.benchmark.exec_time}',
               f'--max-rate={self.benchmark.max_rate}',
               f'--display-every={self.benchmark.status_interval}',
               f'--concurrency={self.benchmark.concurrency}',
               '--tolerate-errors']
        cmd = ' '.join(cmd)
        self.ycsb_process = subprocess.Popen(cmd, shell=True, stdout=open(self.log.runtime,"w"))
        self.start_time = int(time.time()*1e9)
        self.info("Benchmark:ycsb starts. We should consider injecting faults after 30s till the cluster performance is stable", rela=self.start_time)
        # self.info("Benchmark:ycsb starts. Now wait 30s before cluster performance is stable", rela=self.start_time)
        # time.sleep(30)
    
    def _wait_till_benchmark_ends(self):
        self.ycsb_process.wait()
        self.info("Benchmark safely ends", rela=self.start_time)
    
    def _post_process(self):
        p = subprocess.run(['docker-compose', 'logs'], stdout=open(self.log.compose,'w'), stderr =subprocess.STDOUT, cwd=self.tool.compose)

# nw_fault = SlowFault(
#     type_="nw", # nw or fs
#     location_ = "roach1", # e.g., datanode
#     duration_ = 30,
#     severity_ = "slow3",
#     start_time_ = 35)
# fs_fault = SlowFault(
#     type_="fs", # nw or fs
#     location_ = "roach1", # e.g., datanode
#     duration_ = 30,
#     severity_ = "100000",
#     start_time_ = 35)
# b = YCSB_CRDB(exec_time_='150',workload_='a',concurrency_='16')

# t = Crdb(sys_name_= "crdb",
#                fault_ = fs_fault,
#                benchmark_= b,
#                data_dir_= "xixi1")