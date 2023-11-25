from xinda.systems.TestSystem import *

class Mapred(TestSystem):
    def test(self):
        # init
        self.jacoco_loc = 'datanode2'
        self.jacoco_report_dir = self.tool.coverage_dir
        self._jacoco_cleanup()
        self.info(f"Current version: {self.version}")
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
        if self.coverage:
            self._jacoco_export_hadoop_opts()
            self._jacoco_restart()
        # run the mrbench benchmark in background
        self.start_time = int(time.time()*1e9)
        if self.benchmark.benchmark == 'mrbench':
            self.mrbench_run_background()
        elif self.benchmark.benchmark == 'terasort':
            self.terasort_run_background()
        # inject slow faults
        if self.fault.type != 'none':
            self.inject()
        else:
            self.info("Fault type == none, no faults shall be injected")
        # wrap-up and end
        self.info(f"Waiting for the {self.benchmark.workload} jobs to end")
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
               f'hadoop-mapreduce-client-jobclient-{self.version}-tests.jar',
               f"datanode2:/{self.tool.mapred_hadoop_container}"]
        p = subprocess.run(cmd, cwd=self.tool.hadoop_mapreduce_client_local)
        cmd = ['docker',
               'cp',
               f'hadoop-mapreduce-client-jobclient-{self.version}.jar',
               f"datanode2:/{self.tool.mapred_hadoop_container}"]
        p = subprocess.run(cmd, cwd=self.tool.hadoop_mapreduce_client_local)
        cmd = ['docker',
               'cp',
               f'hadoop-mapreduce-examples-{self.version}.jar',
               f"datanode2:/{self.tool.mapred_hadoop_container}"]
        p = subprocess.run(cmd, cwd=self.tool.hadoop_mapreduce_examples_local)
    
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
            # print(raw_log)
            runtime_log = os.path.join(self.log.data_dir, 
                                   'runtime-' + self.fault.location + '-' + self.fault.info + '-' + self.log.iter + "-mrbench" + str(i) +  ".log")
            # print(runtime_log)
            while not check_mrbench_completion(runtime_log):
                cmd = f"docker exec datanode2 yarn jar {self.tool.mapred_mrbench_on_container} mrbench -reduces {self.benchmark.num_reduces}"
                self.info(f"{i} begins /{self.benchmark.num_iter}", rela=self.start_time)
                # try:
                #     _ = subprocess.run(cmd, shell=True, stdout=open(raw_log, "a"), stderr=open(runtime_log, "a"), timeout=60)
                # except subprocess.TimeoutExpired:
                #     self.info(f"TimeoutExpired, {i} FAILed !!!!!", rela=self.start_time)
                # self.info(f"{i} ends /{self.benchmark.num_iter}", rela=self.start_time)
                # if not check_mrbench_completion(runtime_log):
                #     self.info(f"{i} FAILed !!!!!", rela=self.start_time)
                _ = subprocess.run(cmd, shell=True, stdout=open(raw_log, "a"), stderr=open(runtime_log, "a"))
                self.info(f"{i} ends /{self.benchmark.num_iter}", rela=self.start_time)
                if not check_mrbench_completion(runtime_log):
                    self.info(f"{i} FAILed !!!!!", rela=self.start_time)
    
    def _terasort_gen(self):
        raw_log = os.path.join(self.log.data_dir, 'raw-' + self.fault.location + '-' + self.fault.info + '-' + self.log.iter + "-teragen" + ".log")
        runtime_log = os.path.join(self.log.data_dir, 'runtime-' + self.fault.location + '-' + self.fault.info + '-' + self.log.iter + "-teragen" +  ".log")
        cmd = f"docker exec datanode2 yarn jar {self.tool.mapred_terasort_on_container} teragen {self.benchmark.num_of_100_byte_rows} {self.benchmark.input_dir}"
        # try:
        #     _ = subprocess.run(cmd, shell=True, stdout=open(raw_log, "a"), stderr=open(runtime_log, "a"), timeout=60)
        # except subprocess.TimeoutExpired:
        #     self.info(f"TimeoutExpired, teraGEN FAILed !!!!!", rela=self.start_time)
        #     self._terasort_gen()
        _ = subprocess.run(cmd, shell=True, stdout=open(raw_log, "a"), stderr=open(runtime_log, "a"))
    
    def _terasort_sort(self):
        raw_log = os.path.join(self.log.data_dir, 'raw-' + self.fault.location + '-' + self.fault.info + '-' + self.log.iter + "-terasort" + ".log")
        runtime_log = os.path.join(self.log.data_dir, 'runtime-' + self.fault.location + '-' + self.fault.info + '-' + self.log.iter + "-terasort" +  ".log")
        cmd = f"docker exec datanode2 yarn jar {self.tool.mapred_terasort_on_container} terasort {self.benchmark.input_dir} {self.benchmark.output_dir}"
        # try: 
        #     _ = subprocess.run(cmd, shell=True, stdout=open(raw_log, "a"), stderr=open(runtime_log, "a"), timeout=180)
        # except subprocess.TimeoutExpired:
        #     self.info(f"TimeoutExpired, teraSORT FAILed !!!!!", rela=self.start_time)
        #     self._terasort_sort()
        _ = subprocess.run(cmd, shell=True, stdout=open(raw_log, "a"), stderr=open(runtime_log, "a"))
    
    def _terasort(self):
        self._terasort_gen()
        self._terasort_sort()
    
    def terasort_run_background(self):
        self.run_thread = threading.Thread(target=self._terasort)
        self.run_thread.start()


    def mrbench_run_background(self):
        self.run_thread = threading.Thread(target=self._mrbench_run)
        self.run_thread.start()
    
    def _post_process(self):
        p = subprocess.run(['docker-compose', 'logs'], stdout=open(self.log.compose,'w'), stderr =subprocess.STDOUT, cwd=self.tool.compose)
        if self.coverage:
            self._jacoco_get_report()
            # chmod_cmd = "docker exec -it datanode2 chmod -R 777 /jacoco/data /jacoco/reports"
            # _ = subprocess.run(chmod_cmd, shell=True)
            copylogs_cmd = f"docker cp {self.jacoco_loc}:/jacoco/reports/ {self.jacoco_report_dir}"
            _ = subprocess.run(copylogs_cmd, shell=True)
            self.info('jacoco reports retrieved')
            self._jacoco_cleanup()
    
    def _jacoco_cleanup(self):
        cleanup_cmd = f"sudo rm -rf {self.tool.jacoco}/data {self.tool.jacoco}/reports"
        _ = subprocess.run(cleanup_cmd, shell=True)
    
    def _jacoco_export_hadoop_opts(self):
        export_cmd = f"docker exec -it {self.jacoco_loc} sh -c 'echo export HADOOP_OPTS=\"-javaagent:/jacoco/lib/jacocoagent.jar=destfile=/jacoco/data/out.exec,classdumpdir=/jacoco/data/dump -Djacoco-agent.attach=true \$HADOOP_OPTS\" >> /etc/hadoop/hadoop-env.sh'"
        _ = subprocess.run(export_cmd, shell=True)
        # self.info("export HADOOP_OPTS=\"-javaagent:/jacoco/lib/jacocoagent.jar=destfile=/jacoco/data/out.exec,classdumpdir=/jacoco/data/dump -Djacoco-agent.attach=true \$HADOOP_OPTS\" >> /etc/hadoop/hadoop-env.sh")
        tail_cmd = f"docker exec {self.jacoco_loc} tail /etc/hadoop/hadoop-env.sh -n 1"
        p = subprocess.run(tail_cmd, shell=True, stdout=subprocess.PIPE)
        self.info(p.stdout.decode('utf-8').strip())
    
    def _jacoco_restart(self):
        cmd = f"docker restart {self.jacoco_loc}"
        _ = subprocess.run(cmd, shell=True)
        self._docker_status_checker()
    
    def _jacoco_get_report(self):
        if self.version == '3.3.6':
            '''
            The following files have classes with redundant names. In this case, JaCoCo will throw an exception like this: 
                Caused by: java.lang.IllegalStateException: Can't add different class with same name,
            causing some modules to fail to generate reports.
            Removing them will solve the problem.
            For 3.2.1, there will be no exceptions though.
            Most of the files are not critical, despite `client/hadoop-client-runtime-3.3.6.jar`. But all of them have zero coverage in 3.2.1, so we remove them in 3.3.6 as well.
            '''
            file_paths = [
                "/opt/hadoop-3.3.6/share/hadoop/yarn/lib/bcprov-jdk15on-1.68.jar",
                "/opt/hadoop-3.3.6/share/hadoop/yarn/lib/jakarta.xml.bind-api-2.3.2.jar",
                "/opt/hadoop-3.3.6/share/hadoop/yarn/lib/snakeyaml-2.0.jar",
                "/opt/hadoop-3.3.6/share/hadoop/yarn/hadoop-yarn-applications-catalog-webapp-3.3.6.war",
                "/opt/hadoop-3.3.6/share/hadoop/client/hadoop-client-runtime-3.3.6.jar"]
            for file in file_paths:
                mv_cmd = f"docker exec -it {self.jacoco_loc} mv {file} /"
                _ = subprocess.run(mv_cmd, shell=True)
            self.info(f"version:{self.version}: Removed files with redundant classes on {self.jacoco_loc} for generating jacoco reports.")
        elif self.version == '3.0.0':
            file_paths = ['/opt/hadoop-3.0.0/share/hadoop/common/lib/hamcrest-core-1.3.jar',
                          'opt/hadoop-3.0.0/share/hadoop/yarn/lib/jasper-compiler-5.5.23.jar',
                          '/opt/hadoop-3.0.0/share/hadoop/yarn/lib/jasper-runtime-5.5.23.jar']
            for file in file_paths:
                mv_cmd = f"docker exec -it {self.jacoco_loc} mv {file} /"
                _ = subprocess.run(mv_cmd, shell=True)
            self.info(f"version:{self.version}: Removed files with redundant classes on {self.jacoco_loc} for generating jacoco reports.")
        for module in ['client', 'common', 'hdfs', 'mapreduce', 'tools', 'yarn']:
            cmd = f"docker exec -it {self.jacoco_loc} java -jar /jacoco/lib/jacococli.jar report /jacoco/data/out.exec --classfiles /opt/hadoop-{self.version}/share/hadoop/{module} --html /jacoco/reports/{module}"
            _ = subprocess.run(cmd, shell=True)
            self.info(f'Module:{module}: jacoco reports generated', rela=self.start_time)
        # cmd = f"docker exec -it {self.jacoco_loc} java -jar /jacoco/lib/jacococli.jar report /jacoco/data/out.exec --classfiles /opt/hadoop-{self.version}/share/hadoop --html /jacoco/reports/hadoop"
        # _ = subprocess.run(cmd, shell=True)
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

# python3 /users/rmlu/workdir/xinda/main.py --sys_name hadoop --data_dir newv --fault_type nw --fault_location datanode --fault_duration 10 --fault_severity slow-low --fault_start_time 10 --bench_exec_time 150 --benchmark mrbench --coverage --version 3.0.0
# python3 /users/rmlu/workdir/xinda/main.py --sys_name hadoop --data_dir newv --fault_type fs --fault_location datanode --fault_duration 10 --fault_severity 10000 --fault_start_time 10 --bench_exec_time 150 --benchmark mrbench --coverage --version 3.0.0
# python3 /users/rmlu/workdir/xinda/main.py --sys_name hadoop --data_dir newv --fault_type fs --fault_location namenode --fault_duration 10 --fault_severity 10000 --fault_start_time 10 --bench_exec_time 150 --benchmark mrbench --coverage --version 3.0.0