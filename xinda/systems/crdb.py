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
        if self.benchmark.benchmark == 'ycsb':
            # load and run benchmark
            self._load_ycsb()
            self._run_ycsb()
        elif self.benchmark.benchmark == 'sysbench':
            # init (create table)
            self._sysbench_init()
            # load and run benchmark
            self._sysbench_load()
            self._sysbench_run()
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
        if self.cluster_size == 3:
            time.sleep(20)
        elif self.cluster_size == 10:
            time.sleep(40)
        elif self.cluster_size == 20:
            time.sleep(60)
        cmd = 'docker exec -it roach0 ./cockroach --host=roach1:26357 init --insecure'
        _ = subprocess.run(cmd, shell=True)
    
    def _load_ycsb(self):
        if int(self.benchmark.recordcount) > 10000:
            loadThreadCount = 32
            loadTimeout = 120
        else:
            loadThreadCount = 8
            loadTimeout = 60
        cmd = ['docker exec -it roach0',
               './cockroach workload init ycsb',
               f'--insert-count {self.benchmark.recordcount}',
               f'--concurrency {loadThreadCount}',
               '--drop',
               self.benchmark.load_connection_string]
        cmd = ' '.join(cmd)
        p = subprocess.run(cmd, shell=True, timeout=loadTimeout)
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
        self.benchmark_process = subprocess.Popen(cmd, shell=True, stdout=open(self.log.runtime,"w"))
        self.start_time = int(time.time()*1e9)
        self.info("Benchmark:ycsb starts. We should consider injecting faults after 30s till the cluster performance is stable", rela=self.start_time)
    
    def _wait_till_benchmark_ends(self):
        self.info("Wait until benchmark ends", rela=self.start_time)
        self.benchmark_process.wait()
        self.info("Benchmark safely ends", rela=self.start_time)
    
    def _post_process(self):
        log_dict = [
            {'log_on_container': '/cockroach/cockroach-data/logs/cockroach.log', 'log_on_host': self.log.crdb_log},
            {'log_on_container': '/cockroach/cockroach-data/logs/cockroach-pebble.log', 'log_on_host': self.log.crdb_pebble_log},
            {'log_on_container': '/cockroach/cockroach-data/logs/cockroach-health.log', 'log_on_host': self.log.crdb_health_log},
            {'log_on_container': '/cockroach/cockroach-data/logs/cockroach-stderr.log', 'log_on_host': self.log.crdb_stderr_log}
        ]
        for log in log_dict:
            get_symlink_cmd = f'docker exec {self.fault.location} readlink {log["log_on_container"]}'
            p = subprocess.run(get_symlink_cmd, shell=True, stdout=subprocess.PIPE)
            symlink = '/cockroach/cockroach-data/logs/' + p.stdout.decode('utf-8').strip()
            get_reallog_cmd = f'docker cp {self.fault.location}:{symlink} {log["log_on_host"]}'
            p = subprocess.run(get_reallog_cmd, shell=True)
    
    def _sysbench_init(self):
        cmd = "docker exec -i roach0 ./cockroach sql --host=roach1:26257 --insecure"
        process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sql_command = "CREATE DATABASE testdb;\n"
        process.stdin.write(sql_command.encode())
        process.stdin.flush()  # Flush the input to ensure the command is sent
        output, error = process.communicate()
        if process.returncode == 0:
            self.info("database:testdb created succesfully on crdb shell")
        else:
            self.docker_down()
            if self.fault.type == 'nw':
                self.blockade_down()
            elif self.fault.type == 'fs':
                self.charybdefs_down()
            raise EnvironmentError("Error creating database:testdb on crdb shell")
    
    def _sysbench_load(self):
        cmd = ['docker run --rm -it --network=docker-crdb_roachnet rmlu/sysbench:latest',
               'src/sysbench',
               f'src/lua/{self.benchmark.lua_scheme}.lua',
               '--pgsql-host=roach3',
               '--pgsql-port=26257',
               '--pgsql-db=testdb',
               '--pgsql-user=root',
               '--pgsql-password=',
               f'--table_size={self.benchmark.table_size}',
               f'--tables={self.benchmark.num_table}',
               f'--threads={self.benchmark.num_thread}',
               '--db-driver=pgsql',
               'prepare']
        cmd = ' '.join(cmd)
        _ = subprocess.run(cmd, shell=True)
        self.info("./cockroach sysbench workload successfully loaded")
    
    def _sysbench_run(self):
        cmd = ['docker run --rm -it --network=docker-crdb_roachnet rmlu/sysbench:latest',
               'src/sysbench',
               f'src/lua/{self.benchmark.lua_scheme}.lua',
               '--pgsql-host=roach3',
               '--pgsql-port=26257',
               '--pgsql-db=testdb',
               '--pgsql-user=root',
               '--pgsql-password=',
               f'--table_size={self.benchmark.table_size}',
               f'--tables={self.benchmark.num_table}',
               f'--threads={self.benchmark.num_thread}',
               '--db-driver=pgsql',
               f'--time={self.benchmark.exec_time}',
               f'--report-interval={self.benchmark.report_interval}',
               'run']
        cmd = ' '.join(cmd)
        self.benchmark_process = subprocess.Popen(cmd, shell=True, stdout=open(self.log.runtime, 'a'))
        self.start_time = int(time.time()*1e9)
        self.info(f"Benchmark:sysbench {self.benchmark.lua_scheme} starts.", rela=self.start_time)
