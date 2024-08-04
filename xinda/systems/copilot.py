from xinda.systems.TestSystem import *

class Copilot(TestSystem):
    def test(self):
        self.control = "control"
        # init
        self.info(self.fault.get_info(), if_time=False)
        if self.fault.type == 'nw':
            self.docker_up()
            time.sleep(10)
            self.info("A new cluster is properly set up.")
            self.docker_get_status()
            self.blockade_up()
        elif self.fault.type == 'fs':
            self.charybdefs_up()
            self.docker_up()
            time.sleep(10)
            self.info("A new cluster is properly set up.")
            self.docker_get_status()
        elif self.fault.type == 'none':
            self.docker_up()
            time.sleep(10)
            self.info("A new cluster is properly set up.")
            self.docker_get_status()
        else:
            raise ValueError(f"Fault type:{self.fault.type} is not one of {{nw, fs, none}}")
        self._init_copilot()
        # run benchmark
        self._run_copilot()
        # inject slow faults
        if self.fault.type != 'none':
            '''
            We need to sleep for approximately 20s since it takes some time for copilot's internal activities like master/replica set up.
            However, I do think this can be fixed: maybe we can emit some signal in copilot/startexpt.sh to indicate that the benchmark is running and then we inject the slow faults. Or, we separate copilot/startexpt.sh as two
            '''
            self.sleep(20)
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
        self.info(f"Log absolute path: {self.log.data_dir}")
        self.info("THE END")
        

    def _init_copilot(self):
        cmd = ["./config.sh"]
        p = subprocess.run(cmd, shell=True, cwd=self.tool.compose)
        self.info("copilot initiated.")
        self.info(f'copilot_scheme: {self.benchmark.scheme}')
        self.info(f'copilot_nclient: {self.benchmark.nclient}')
        self.info(f'copilot_concurrency: {self.benchmark.concurrency}')
    
    def _run_copilot(self):
        cmd = f"docker exec -it {self.control} bash startexpt.sh {self.benchmark.scheme} 3 {self.benchmark.concurrency} {self.benchmark.nclient} {self.benchmark.exec_time} {self.benchmark.trim_ratio}"
        self.copilot_process = subprocess.Popen(cmd, shell=True, stdout=open(self.log.compose,"w"))
        self.start_time = int(time.time()*1e9)
        self.info(f"Benchmark:copilot, scheme:{self.benchmark.scheme} starts.", rela=self.start_time)
    
    def _wait_till_benchmark_ends(self):
        self.info("Wait until benchmark ends", rela=self.start_time)
        self.copilot_process.wait()
        self.info("Benchmark safely ends", rela=self.start_time)
    
    def _post_process(self):
        data_dir = '/root/code/copilot/experiments/latest'
        
        cmd = f"docker cp {self.control}:{data_dir}/percentilesnew.txt {self.log.copilot_latency_percentage}"
        p = subprocess.run(cmd, cwd=self.log.data_dir, shell=True)
        
        cmd = f"docker cp {self.control}:{data_dir}/sys_tput.txt {self.log.copilot_aggregated_throughput}"
        p = subprocess.run(cmd, cwd=self.log.data_dir, shell=True)
        
        cmd = f"docker exec -it {self.control} bash -c 'rm {data_dir}/percentilesnew.txt {data_dir}/sys_tput.txt'"
        p = subprocess.run(cmd, shell=True)
        cmd = f"docker cp {self.control}:{data_dir} {self.log.copilot_misc}"
        p = subprocess.run(cmd, cwd=self.log.data_dir, shell=True)
        self.info("Data post-processed.")

# nw-slow - copilot
# python3 /users/rmlu/workdir/xinda/main.py --sys_name copilot --data_dir test --fault_type nw --fault_location replica1 --fault_duration 50 --fault_severity slow-100ms --fault_start_time 20 --bench_exec_time 90 --benchmark copilot --copilot_concurrency 10 --copilot_scheme copilot --iter 1 --log_root_dir /users/rmlu/workdir/data/copilot_test_$(date "+%m%d_%H%M")