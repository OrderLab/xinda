from xinda.systems.TestSystem import *

class Depfast(TestSystem):
    def test(self):
        self.client = "client"
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
        self._init_depfast()
        # run benchmark
        self._run_depfast()
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
        self.info(f"Log absolute path: {self.log.data_dir}")
        self.info("THE END")
        

    def _init_depfast(self):
        cmd = ["./config.sh"]
        p = subprocess.run(cmd, shell=True, cwd=self.tool.compose)
        self.info("depfast initiated.")
        self.info(f'depfast_scheme: {self.benchmark.scheme}')
        self.info(f'depfast_nclient: {self.benchmark.nclient}')
        self.info(f'depfast_concurrency: {self.benchmark.concurrency}')
    
    def check_if_benchmark_starts(self):
        cmd = f"docker exec -it {self.client} test -f /root/code/depfast/docker/ifBenchmarkStarts"
        p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
        return p.returncode == 0
    
    def _run_depfast(self):
        # depfast_slow_location = ''
        # if self.fault.location == 'server1':
        #     depfast_slow_location = 'leader'
        # elif self.fault.location == 'server3':
        #     depfast_slow_location = 'follower'
        # else:
        #     raise ValueError(f"Exception: fault physical location ({self.fault.location}) does not match depfast topology (not {depfast_slow_location})")
        # self.info(f"fault_physical_location: {self.fault.location}, which is {depfast_slow_location} in depfast\'s toplogy ")
        cmd = f"docker exec -it {self.client} bash start-exp.sh testname {self.benchmark.exec_time} 0 3 follower {self.benchmark.nclient} {self.benchmark.concurrency} {self.benchmark.scheme} nonlocal"
        self.depfast_process = subprocess.Popen(cmd, shell=True, stdout=open(self.log.runtime,"w"))
        self.info(f"Wait for depfast to start.")
        sleep_time = 0
        while True:
            if self.check_if_benchmark_starts():
                break
            else:
                print(f"{sleep_time}s> depfast-{self.benchmark.scheme} not started yet. Sleep for 1s")
                time.sleep(1)
                sleep_time += 1
            if sleep_time >= 30:
                raise Exception(f"scheme:{self.benchmark.scheme} never starts after {self.sleep_time}s timeout")
        self.start_time = int(time.time()*1e9)
        self.info(f"Benchmark:depfast, scheme:{self.benchmark.scheme} starts.", rela = self.start_time)
    
    def _wait_till_benchmark_ends(self):
        depfast_timeout = int(self.benchmark.exec_time) - int((int(time.time()*1e9) - self.start_time)/1e9) + 90
        self.info(f"Wait until benchmark ends (timeout: {depfast_timeout}s)", rela=self.start_time)
        try:
            self.depfast_process.wait(timeout=depfast_timeout)
            self.info("Benchmark safely ends", rela=self.start_time)
        except:
            self.info(f"The subprocess took too long (>={depfast_timeout}s) to complete and was killed.", rela=self.start_time)
            self.depfast_process.kill()
    
    def _post_process(self):
        # p = subprocess.run(['docker-compose', 'logs'], stdout=open(self.log.compose,'w'), stderr =subprocess.STDOUT, cwd=self.tool.compose)
        # Rename experiment results
        cmd = f"docker exec -it {self.client} bash -c \'mv results/*.yml {self.log.depfast_summary}; mv log {self.log.depfast_misc};\'"
        p = subprocess.run(cmd, shell=True)
        # copy the summary yaml
        cmd = f"docker cp {self.client}:/root/code/depfast/{self.log.depfast_summary} ."
        p = subprocess.run(cmd, cwd=self.log.data_dir, shell=True)
        # copy misc logs
        cmd = f"docker cp {self.client}:/root/code/depfast/{self.log.depfast_misc} ."
        p = subprocess.run(cmd, cwd=self.log.data_dir, shell=True)
        # append concurrency levels to the summary yaml
        with open(os.path.join(self.log.data_dir, self.log.depfast_summary), 'a') as file:
            file.write(f'CONCURRENCY: {self.benchmark.concurrency}\n')
        self.info("Data post-processed.")

# None
# python3 /users/rmlu/workdir/xinda/main.py --sys_name depfast --data_dir test --fault_type nw --fault_location server1 --fault_duration -1 --fault_severity slow-100ms --fault_start_time 10 --bench_exec_time 10 --benchmark depfast --depfast_concurrency 100 --iter 1 --log_root_dir /users/rmlu/workdir/data/depfast_none_$(date "+%m%d_%H%M")

# nw-slow
# python3 /users/rmlu/workdir/xinda/main.py --sys_name depfast --data_dir test --fault_type nw --fault_location server1 --fault_duration 60 --fault_severity slow-100ms --fault_start_time 10 --bench_exec_time 60 --benchmark depfast --depfast_concurrency 100 --iter 1 --log_root_dir /users/rmlu/workdir/data/depfast_nwslow_$(date "+%m%d_%H%M")
# python3 /users/rmlu/workdir/xinda/main.py --sys_name depfast --data_dir test --fault_type nw --fault_location server1 --fault_duration 60 --fault_severity slow-10ms --fault_start_time 10 --bench_exec_time 60 --benchmark depfast --depfast_concurrency 100 --iter 1 --log_root_dir /users/rmlu/workdir/data/depfast_nwslow_$(date "+%m%d_%H%M")

# python3 /users/rmlu/workdir/xinda/main.py --sys_name depfast --data_dir test --fault_type nw --fault_location server1 --fault_duration 60 --fault_severity slow-40ms --fault_start_time 10 --bench_exec_time 60 --benchmark depfast --depfast_concurrency 1 --iter 1 --log_root_dir /users/rmlu/workdir/data/depfast_nwslow_$(date "+%m%d_%H%M") --depfast_scheme copilot