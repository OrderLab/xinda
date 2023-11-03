from xinda.systems.TestSystem import *

class Mapred(TestSystem):
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
            time.sleep(10)
        else:
            raise ValueError(f"Fault type:{self.fault.type} is not one of {{nw, fs}}")
        self._copy_file_to_container()
        # run the mrbench benchmark in background
        self.start_time = int(time.time()*1e9)
        self.mrbench_run_background()
        # inject slow faults
        if self.fault.type != 'none':
            self.inject()
        else:
            self.info("Fault type == none, no faults shall be injected")
        # wrap-up and end
        self.info("Waiting for the mrbench jobs to end")
        self.run_thread.join()
        self._post_process()
        self.docker_down()
        if self.fault.type == 'nw':
            self.blockade_down()
        elif self.fault.type == 'fs':
            self.charybdefs_down()
        self.info("THE END")
    
    def _docker_status_checker(self):
        cmd = ["docker exec -it namenode hdfs dfsadmin -report | grep 'Live datanodes ' |grep -oP '\(.*\)' | tr -d '()'"]
        while True:
            num_live_datanode = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout.strip()
            if num_live_datanode == b'3':
                self.info("We have 3 live datanodes now.")
                break
            else:
                print("Still waiting for cluster to set up. Sleep 10s")
                time.sleep(10)
        cmd = ["docker ps -a | grep '(healthy)' | wc -l"]
        while True:
            num_healthy_node = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout.strip()
            if num_healthy_node == b'9':
                self.info("Hadoop cluster properly set up.")
                break
            else:
                print("Still waiting for cluster to set up. Sleep 10s")
                time.sleep(10)
        self.docker_get_status()
    
    def _copy_file_to_container(self):
        cmd = ['docker',
               'cp',
               'hadoop-mapreduce-client-jobclient-3.2.1-tests.jar',
               f"datanode2:/{self.tool.mapred_hadoop_container}"]
        p = subprocess.run(cmd, cwd=self.tool.mapred_hadoop_local)
        cmd = ['docker',
               'cp',
               'hadoop-mapreduce-client-jobclient-3.2.1.jar',
               f"datanode2:/{self.tool.mapred_hadoop_container}"]
        p = subprocess.run(cmd, cwd=self.tool.mapred_hadoop_local)
    
    def _mrbench_run(self):
        def check_mrbench_completion(log_file):
            try:
                with open(log_file, 'r') as f:
                    log_contents = f.read()
            except FileNotFoundError:
                log_contents = ""
            return "END-OF-MRBench" in log_contents
        print(self.benchmark.num_iter)
        for i in range(1, self.benchmark.num_iter+1):
            raw_log = os.path.join(self.log.data_dir, 
                                   'raw-' + self.fault.location + '-' + self.fault.info + '-' + self.log.iter + "-mrbench" + ".log")
            print(raw_log)
            runtime_log = os.path.join(self.log.data_dir, 
                                   'runtime-' + self.fault.location + '-' + self.fault.info + '-' + self.log.iter + "-mrbench" + str(i) +  ".log")
            print(runtime_log)
            while not check_mrbench_completion(runtime_log):
                cmd = f"docker exec datanode2 yarn jar {self.tool.mapred_mrbench_on_container} mrbench -reduces {self.benchmark.num_reduces}"
                self.info(f"{i} begins /{self.benchmark.num_iter}", rela=self.start_time)
                _ = subprocess.run(cmd, shell=True, stdout=open(raw_log, "a"), stderr=open(runtime_log, "a"))
                self.info(f"{i} ends /{self.benchmark.num_iter}", rela=self.start_time)
                if not check_mrbench_completion(runtime_log):
                    self.info(f"{i} FAILed !!!!!", rela=self.start_time)
    
    def mrbench_run_background(self):
        self.run_thread = threading.Thread(target=self._mrbench_run)
        self.run_thread.start()
    
    def _post_process(self):
        p = subprocess.run(['docker-compose', 'logs'], stdout=open(self.log.compose,'w'), stderr =subprocess.STDOUT, cwd=self.tool.compose)

# nw_fault = SlowFault(
#     type_="nw", # nw or fs
#     location_ = "datanode", # e.g., datanode
#     duration_ = 20,
#     severity_ = "slow3",
#     start_time_ = 5)
# fs_fault = SlowFault(
#     type_="fs", # nw or fs
#     location_ = "datanode", # e.g., datanode
#     duration_ = 20,
#     severity_ = "100000",
#     start_time_ = 5)
# b = MRBENCH_MAPRED(num_reduces_='3',
#                    num_iter_=3)

# t = Mapred(sys_name_= "hadoop",
#                fault_ = nw_fault,
#                benchmark_= b,
#                data_dir_= "xixi1")