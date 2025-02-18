from xinda.systems.TestSystem import *
import signal
import psutil
import math

class Kafka(TestSystem):
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
            time.sleep(20)
        elif self.fault.type == 'none':
            self.docker_up()
            time.sleep(20)
        else:
            raise ValueError(f"Fault type:{self.fault.type} is not one of {{nw, fs}}")
        if self.benchmark.benchmark == 'perf_test':
            # create a test kafka topic
            self.init_kafka()
            # run basic-benchmark:consumer first
            self.basic_consumer()
            time.sleep(5)
            # then run basic-benchmark:producer
            self.basic_producer()
            '''
            Currently, since the workload is heavy (50%+ cpu consumed), blockade cmds will take ~25s to finish
            '''
            self.start_time = int(time.time()*1e9)
            self.inject()
            # wrap-up and end
            self._wait_till_perftest_ends()
        elif self.benchmark.benchmark == 'openmsg':
            self._openmsg_change_test_duration()
            self._openmsg_run_worker1()
            self._openmsg_run_worker2()
            self._openmsg_run_driver()
            self._openmsg_check_if_warmup_ends()
            self.start_time = int(time.time()*1e9)
            self.inject()
            # wrap-up and end
            self._wait_till_openmsg_ends()
        else:
            raise ValueError(f"Benchmark: {self.benchmark.workload} is not one of {{perf_test, openmsg}}")
        self._post_process()
        self.docker_down()
        if self.fault.type == 'nw':
            self.blockade_down()
        elif self.fault.type == 'fs':
            self.charybdefs_down()
        self.info("THE END")
    
    def init_kafka(self):
        cmd = f"docker cp {self.tool.kafka_compiled_source} kafka-benchmarking:/"
        _ = subprocess.run(cmd, shell=True)
        self.info("Copy compiled kafka source to kafka-benchmarking:/kafka")
        cmd = ['docker exec -it kafka-benchmarking',
               'sh /kafka/bin/kafka-topics.sh',
               '--create --bootstrap-server kafka1:9092',
               f'--replication-factor {self.benchmark.replication_factor}',
               f'--partitions {self.benchmark.topic_partition}',
               f'--topic {self.benchmark.topic_title}']
        cmd = ' '.join(cmd)
        _ = subprocess.run(cmd, shell=True)
        self.info(f"Kafka topic:{self.benchmark.topic_title} created")
    
    def basic_producer(self):
        cmd = ['docker exec kafka-benchmarking',
        'sh /kafka/bin/kafka-producer-perf-test.sh',
        '--topic test-xinda',
        f'--num-records {self.benchmark.num_msg}',
        '--producer-props bootstrap.servers=kafka1:9092,kafka2:9092,kafka3:9092,kafka4:9092',
        f'--throughput {self.benchmark.throughput_upper_bound}',
        '--record-size 1024',
        '--reporting-interval 1000'] # report every 1 second
        # --num-records 1500000 + --throughput 10000
        # --num-records 14000000 + --throughput -1
        # 14M records will run in ~150s, taking up 54GB disk space
        # If we set scheduled cleanups at given frequency (see docker-compose.yml), the runtime performance will be affected (100 MB/s => < 10MB/s) and thus not worth it. So, make sure that the home directory has >60GB disk space.
        cmd = ' '.join(cmd)
        self.info("[PRODUCER] kafka-producer-perf-test.sh started", rela=self.start_time)
        self.producer_process = subprocess.Popen(cmd, shell=True, stdout=open(self.log.kafka_producer, 'a'), stderr=subprocess.DEVNULL)
    
    def basic_consumer(self):
        cmd = ['docker exec kafka-benchmarking',
        'sh /kafka/bin/kafka-consumer-perf-test.sh',
        '--bootstrap-server kafka1:9092,kafka2:9092,kafka3:9092,kafka4:9092',
        f'--messages {self.benchmark.num_msg}',
        '-reporting-interval 1000',
        '--show-detailed-stats',
        '--topic test-xinda',
        '--timeout 10000']
        cmd = ' '.join(cmd)
        self.info("[CONSUMER] kafka-consumer-perf-test.sh started", rela=self.start_time)
        self.consumer_process = subprocess.Popen(cmd, shell=True, stdout=open(self.log.kafka_consumer, 'a'), stderr=subprocess.DEVNULL)
    
    def _wait_till_perftest_ends(self):
        self.producer_process.poll()
        cur_time = self.get_current_ts()
        if cur_time < self.benchmark.exec_time and self.producer_process.returncode != 0:
            self.info(f"Sleep {self.benchmark.exec_time - cur_time}s till the end", rela=self.start_time)
            time.sleep(self.benchmark.exec_time - cur_time)
        self.producer_process.terminate()
        self.consumer_process.terminate()
        self.info("Benchmark safely ends", rela=self.start_time)
    
    def _wait_till_openmsg_ends(self):
        self.driver_process.poll()
        self.worker1_process.poll()
        self.worker2_process.poll()
        counter = 0
        while True:
            if self.check_string_in_file(file_path=self.log.openmsg_driver, target_string="Writing test result"):
                # self.info("Benchmark ends!")
                break
            time.sleep(10) # check every 0.2s 
            counter = counter + 10
            cur_time = self.get_current_ts()
            self.info(f"Waiting for benchmark to end. Sleep 10s / Elapsed {counter}s / Need at most ~{self.benchmark.exec_time - cur_time}s)", rela=self.start_time)
            if counter >= self.benchmark.exec_time + 300:
                self.info(f"FATAL: benchmark does not end even after {self.benchmark.exec_time}+300={self.benchmark.exec_time + 30}s")
                exit(1)
        process = psutil.Process(self.driver_process.pid)
        for proc in process.children(recursive=True):
            proc.kill()
        process.kill()
        self.worker1_process.send_signal(signal.SIGINT)
        self.worker2_process.send_signal(signal.SIGINT)
        if self.is_port_in_use([8082,8083,8084,8085]):
            self.info("Kill all processes running on port 8082,8083,8084,8085", rela=self.start_time)
            # cmd = "ps aux | grep -e ':8082' -e ':8084' -e 'port 8082' -e 'port 8084' | awk '{print $2}' | xargs kill -9"
            cmd = 'lsof -i :8082 -i :8083 -i :8084 -i :8085 -t | xargs -r kill -9'
            _ = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.info("Benchmark safely ends", rela=self.start_time)
    
    def _openmsg_change_test_duration(self):
        # change the testDurationMinutes field in the openmsg workload file
        with open(os.path.join(self.tool.openmsg_compiled_source, f"workloads/{self.benchmark.workload_file}.yaml"), 'r') as file:
            data = yaml.safe_load(file)
        new_exec_time = math.ceil(self.benchmark.exec_time/60)
        self.info(f"Execution time will be rounded: {self.benchmark.exec_time}s -> {new_exec_time}min*60={new_exec_time*60}s")
        self.benchmark.change_exec_time(new_exec_time*60)
        data['testDurationMinutes'] = new_exec_time
        with open(os.path.join(self.tool.openmsg_compiled_source, "workloads/this.yaml"), 'w') as file:
            yaml.dump(data, file, default_flow_style=False)
        self.info(f"{self.tool.openmsg_compiled_source}/workloads/this.yaml created")
        
    
    def _openmsg_run_driver(self):
        cmd = ['bin/benchmark',
        f'--drivers driver-kafka/{self.benchmark.driver}.yaml',
        '--workers http://0.0.0.0:8082,http://0.0.0.0:8084',
        f'workloads/this.yaml']
        # kafka-latency.yaml has (nearly) the same configs as kafka.yaml in previous commits. kafka.yaml is said to be the standard configs.
        # https://github.com/openmessaging/benchmark/blob/211cbcd436b022d1734d8d1d9e760b34a05f4488/driver-kafka/kafka.yaml
        cmd = ' '.join(cmd)
        self.driver_process = subprocess.Popen('exec ' + cmd, shell=True, stdout=open(self.log.openmsg_driver, 'a'), cwd=self.tool.openmsg_compiled_source)
    
    def _openmsg_run_worker1(self):
        cmd = ['bin/benchmark-worker',
        '--port 8082',
        '--stats-port 8083']
        cmd = ' '.join(cmd)
        self.worker1_process = subprocess.Popen('exec ' + cmd, shell=True, stdout=open(self.log.openmsg_worker1, 'a'), cwd=self.tool.openmsg_compiled_source)
    
    def _openmsg_run_worker2(self):
        cmd = ['bin/benchmark-worker',
        '--port 8084',
        '--stats-port 8085']
        cmd = ' '.join(cmd)
        self.worker2_process = subprocess.Popen('exec ' + cmd, shell=True, stdout=open(self.log.openmsg_worker2, 'a'), cwd=self.tool.openmsg_compiled_source)
    
    def check_string_in_file(self, file_path, target_string):
        with open(file_path, 'r') as file:
            if target_string in file.read():
                return True
            else:
                return False
    
    def _openmsg_check_if_warmup_ends(self):
        self.info("Waiting for warm-up period to end")
        counter = 0
        time.sleep(50)
        while True:
            if self.check_string_in_file(file_path=self.log.openmsg_driver, target_string="Starting benchmark traffic"):
                self.info("Warm-up period ends!")
                return True
            time.sleep(0.2) # check every 0.2s 
            counter = counter + 0.2
            if counter >= 120:
                self.info("Warm-up period does not end in 120s. Abort.")
                exit(1)
    
    def _post_process(self):
        p = subprocess.run(['docker-compose', 'logs'], stdout=open(self.log.compose,'w'), stderr =subprocess.STDOUT, cwd=self.tool.compose)
        p = subprocess.run(f'mv *.json {self.log.openmsg_summary}', shell=True, stdout=open(self.log.openmsg_worker1, 'a'), cwd=self.tool.openmsg_compiled_source)