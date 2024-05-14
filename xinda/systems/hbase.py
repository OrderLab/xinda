from xinda.systems.TestSystem import *

class HBase(TestSystem):
    def test(self):
        # init
        self.jacoco_loc = 'hbase-regionserver'
        self.jacoco_report_dir = self.tool.coverage_dir
        self._jacoco_cleanup()
        self.dest = 'hbase-regionserver2'
        self.info(self.fault.get_info(), if_time=False)
        if self.fault.type == 'nw':
            self.docker_up()
            time.sleep(60)
            self.info("A new cluster is properly set up.")
            self.docker_get_status()
            self.blockade_up()
        elif self.fault.type == 'fs':
            self.charybdefs_up()
            self.docker_up()
            time.sleep(60)
            self.info("A new cluster is properly set up.")
            self.docker_get_status()
        elif self.fault.type == 'none':
            self.docker_up()
            time.sleep(60)
            self.info("A new cluster is properly set up.")
            self.docker_get_status()
        else:
            raise ValueError(f"Fault type:{self.fault.type} is not one of {{nw, fs}}")
        self._copy_file_to_container()
        if self.coverage:
            self._jacoco_export_hbase_opts()
            self._jacoco_restart()
        self._init_hbase()
        self._load_ycsb()
        self.start_time = int(time.time()*1e9)
        # inject slow faults (in a background thread)
        if self.fault.type != 'none':
            self.inject()
        else:
            self.info("Fault type == none, no faults shall be injected")
        self._run_ycsb()
        # wrap-up and end
        if self.fault.type != 'none':
            self.inject_thread.join()
        # self._wait_till_benchmark_ends()
        self._post_process()
        self.docker_down()
        if self.fault.type == 'nw':
            self.blockade_down()
        elif self.fault.type == 'fs':
            self.charybdefs_down()
        self.info("THE END")
    
    def _copy_file_to_container(self):
        cmd = ['docker',
               'cp',
               self.tool.hbase_init,
               f"{self.dest}:/tmp/hbase-init.sh"]
        p = subprocess.run(cmd)
        cmd = ['docker',
               'cp',
               self.tool.hbase_check_pid,
               f"{self.dest}:/tmp/hbase-check-pid.sh"]
        p = subprocess.run(cmd)
        cmd = ['docker',
               'cp',
               self.tool.ycsb,
               f"{self.dest}:/tmp/"]
        p = subprocess.run(cmd)
        cmd = ['docker',
               'cp',
               self.tool.ycsb_wkl_root,
               f"{self.dest}:/tmp/"]
        p = subprocess.run(cmd)
    
    def _init_hbase(self):
        cmd = ['docker',
               'exec', '-it',
               self.dest,
               'bash', '/tmp/hbase-init.sh']
        p = subprocess.run(cmd)
        self.info("TABLE:usertable COLUMNFAMILY:family initiated")
    
    def inject(self):
        self.inject_thread = threading.Thread(target=super().inject)
        self.inject_thread.start()
    
    def _load_ycsb(self):
        cmd = ['docker exec -it',
               self.dest,
               'sh -c',
               f'\"{self.tool.hbase_ycsb}/bin/ycsb load hbase20',
               '-s',
            #    f"-P {self.tool.hbase_ycsb}/workloads/workload{self.benchmark.workload}",
               f"-P {self.tool.hbase_ycsb_wkl}/workload{self.benchmark.workload}",
               '-cp /etc/hbase',
               f'-p recordcount={self.benchmark.recordcount}',
               f"-p columnfamily={self.benchmark.columnfamily}\""]
        cmd = ' '.join(cmd)
        p = subprocess.run(cmd, shell=True)
        self.info(f"{self.tool.ycsb}/workloads/workload{self.benchmark.workload} successfully loaded")
    
    def _run_ycsb(self):
        cmd = ['docker exec -it',
               self.dest,
               'sh -c',
               f"\"{self.tool.hbase_ycsb}/bin/ycsb run hbase20",
               '-s',
            #    f"-P {self.tool.hbase_ycsb}/workloads/workload{self.benchmark.workload}",
               f"-P {self.tool.hbase_ycsb_wkl}/workload{self.benchmark.workload}",
               '-cp /etc/hbase',
               f"-p measurementtype={self.benchmark.measurementtype}",
               f"-p operationcount={self.benchmark.operationcount}",
               f"-p maxexecutiontime={self.benchmark.exec_time}",
               f"-p status.interval={self.benchmark.status_interval}",
               f"-p columnfamily={self.benchmark.columnfamily}",
               f"-p threadcount=8",
               f"> {self.log.raw_container}",
               f"2> {self.log.runtime_container}\""]
        cmd = ' '.join(cmd)
        self.info("Benchmark:ycsb starts. We should inject faults after 30s till the cluster performance is stable", rela=self.start_time)
        self.ycsb_process = subprocess.run(cmd, shell=True)
    
    def _wait_till_benchmark_ends(self):
        cmd = ['docker exec -it',
               self.dest,
               'bash /tmp/hbase-check-pid.sh']
        cmd = ' '.join(cmd)
        self.info("Now wait until the benchmark ends", rela=self.start_time)
        p = subprocess.run(cmd, shell=True)
        self.info("Benchmark safely ends", rela=self.start_time)
    
    def _post_process(self):
        p = subprocess.run(['docker-compose', 'logs'], stdout=open(self.log.compose,'w'), stderr =subprocess.STDOUT, cwd=self.tool.compose)
        cmd = f"docker cp {self.dest}:{self.log.raw_container} ."
        p = subprocess.run(cmd, cwd=self.log.data_dir, shell=True)
        cmd = f"docker cp {self.dest}:{self.log.runtime_container} ."
        p = subprocess.run(cmd, cwd=self.log.data_dir, shell=True)
        # Convert raw.log => ts.log
        cmd = f"cat {self.log.raw} | grep -e \"READ,\" -e \"UPDATE,\" -e \"SCAN,\" -e \"INSERT,\" -e \"READ-MODIFY-WRITE,\" > {self.log.time_series}"
        p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Convert raw.log => sum.log
        cmd = f"cat {self.log.raw} | grep -v -e \"READ,\" -e \"UPDATE,\" -e \"SCAN,\" -e \"INSERT,\" -e \"READ-MODIFY-WRITE,\" > {self.log.summary}"
        p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        '''
        for iter in range(self.benchmark.num_cycle):
            # Copy logs to local
            cmd = f"docker cp {self.dest}:{self.log.raw_load_container[iter]} ."
            p = subprocess.run(cmd, cwd=self.log.data_dir, shell=True)
            cmd = f"docker cp {self.dest}:{self.log.runtime_load_container[iter]} ."
            p = subprocess.run(cmd, cwd=self.log.data_dir, shell=True)
            cmd = f"docker cp {self.dest}:{self.log.raw_run_container[iter]} ."
            p = subprocess.run(cmd, cwd=self.log.data_dir, shell=True)
            cmd = f"docker cp {self.dest}:{self.log.runtime_run_container[iter]} ."
            p = subprocess.run(cmd, cwd=self.log.data_dir, shell=True)
    
            # Convert raw.log => ts.log
            cmd = f"cat {self.log.raw_load[iter]} | grep -e \"READ,\" -e \"UPDATE,\" -e \"SCAN,\" -e \"INSERT,\" -e \"READ-MODIFY-WRITE,\" > {self.log.ts_load[iter]}"
            p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            cmd = f"cat {self.log.raw_run[iter]} | grep -e \"READ,\" -e \"UPDATE,\" -e \"SCAN,\" -e \"INSERT,\" -e \"READ-MODIFY-WRITE,\" > {self.log.ts_run[iter]}"
            p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Convert raw.log => sum.log
            cmd = f"cat {self.log.raw_load[iter]} | grep -v -e \"READ,\" -e \"UPDATE,\" -e \"SCAN,\" -e \"INSERT,\" -e \"READ-MODIFY-WRITE,\" > {self.log.sum_load[iter]}"
            cmd = f"cat {self.log.raw_run[iter]} | grep -v -e \"READ,\" -e \"UPDATE,\" -e \"SCAN,\" -e \"INSERT,\" -e \"READ-MODIFY-WRITE,\" > {self.log.sum_run[iter]}"
            p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        '''
        self.info("Convert raw to ts/sum")
        if self.coverage:
            self._jacoco_get_report()
            copylogs_cmd = f"docker cp {self.jacoco_loc}:/jacoco/reports/ {self.jacoco_report_dir}"
            _ = subprocess.run(copylogs_cmd, shell=True)
            self.info('jacoco reports retrieved')
            self._jacoco_cleanup()

    def _jacoco_cleanup(self):
        cleanup_cmd = f"sudo rm -rf {self.tool.jacoco}/data {self.tool.jacoco}/reports"
        _ = subprocess.run(cleanup_cmd, shell=True)
    
    def _jacoco_export_hbase_opts(self):
        # export_cmd = f"docker exec -it {self.jacoco_loc} sh -c 'echo export HBASE_OPTS=\"-javaagent:/jacoco/lib/jacocoagent.jar=destfile=/jacoco/data/out.exec,classdumpdir=/jacoco/data/dump,append=true \$HBASE_OPTS\" >> /etc/hbase/hbase-env.sh'"
        export_cmd = f"docker exec -it {self.jacoco_loc} sh -c 'echo export HBASE_OPTS=\"-javaagent:/jacoco/lib/jacocoagent.jar=address=*,port=36320,destfile=/jacoco/data/out.exec,output=tcpserver \$HBASE_OPTS\" >> /etc/hbase/hbase-env.sh'"
        _ = subprocess.run(export_cmd, shell=True)
        tail_cmd = f"docker exec {self.jacoco_loc} tail /etc/hbase/hbase-env.sh -n 1"
        p = subprocess.run(tail_cmd, shell=True, stdout=subprocess.PIPE)
        self.info(p.stdout.decode('utf-8').strip())
    
    def _jacoco_restart(self):
        cmd = f"docker restart {self.jacoco_loc}"
        _ = subprocess.run(cmd, shell=True)
        time.sleep(60)
    
    def _jacoco_get_report(self):
        module_list = ['hbase-annotations', 'hbase-archetypes', 'hbase-assembly', 'hbase-asyncfs', 'hbase-build-configuration', 'hbase-checkstyle', 'hbase-client', 'hbase-common', 'hbase-compression', 'hbase-endpoint', 'hbase-examples', 'hbase-external-blockcache', 'hbase-hadoop2-compat', 'hbase-hadoop-compat', 'hbase-hbtop', 'hbase-http', 'hbase-it', 'hbase-logging', 'hbase-mapreduce', 'hbase-metrics', 'hbase-metrics-api', 'hbase-procedure', 'hbase-protocol', 'hbase-protocol-shaded', 'hbase-replication', 'hbase-resource-bundle', 'hbase-rest', 'hbase-rsgroup', 'hbase-server', 'hbase-shaded', 'hbase-shell', 'hbase-testing-util', 'hbase-thrift', 'hbase-zookeeper']
        for module in module_list:
            cmd = f"docker exec -it {self.jacoco_loc} java -jar /jacoco/lib/jacococli.jar dump --address localhost --port 36320 --destfile /jacoco/data/out.exec"
            _ = subprocess.run(cmd, shell=True)
            self.info(f'Module:{module}: jacoco out.exec dumped', rela=self.start_time)
            cmd = f"docker exec -it {self.jacoco_loc} java -jar /jacoco/lib/jacococli.jar report /jacoco/data/out.exec --classfiles /opt/hbase-2.5.6/lib/{module}-2.5.6.jar --html /jacoco/reports/{module}"
            _ = subprocess.run(cmd, shell=True)
            self.info(f'Module:{module}: jacoco reports generated', rela=self.start_time)