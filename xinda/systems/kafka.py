from xinda.systems.TestSystem import *
import signal
import psutil

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
            self._openmsg_run_worker1()
            self._openmsg_run_worker2()
            self._openmsg_run_driver()
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
            #    f"--config cleanup.policy='delete'",
            #    f"--config retention.bytes=100000000", # 1GB= 1000000000 bytes
            #    f"--config retention.ms=-1",
            #    f"--config segment.bytes=10000000",
            #    f"--config retention.ms=10000",
            #    f"--config delete.retention.ms=10000",
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
        ## docker exec -it kafka-benchmarking sh /kafka/bin/kafka-topics.sh --bootstrap-server kafka1:9092,kafka2:9092,kafka3:9092,kafka4:9092 --describe --topic test-xinda
        ## docker exec -it kafka-benchmarking sh /kafka/bin/kafka-metadata-quorum.sh --bootstrap-server kafka1:9092 describe --replication
    
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
        return_code = self.driver_process.returncode and self.worker1_process.returncode and self.worker2_process.returncode
        cur_time = self.get_current_ts()
        if cur_time < self.benchmark.exec_time and return_code != 0:
            self.info(f"Sleep {self.benchmark.exec_time - cur_time}s till the end", rela=self.start_time)
            time.sleep(self.benchmark.exec_time - cur_time)
        # process = psutil.Process(self.worker1_process.pid)
        # print(process.children(recursive=True))
        # process = psutil.Process(self.worker2_process.pid)
        # print(process.children(recursive=True))
        process = psutil.Process(self.driver_process.pid)
        # print(process.children(recursive=True))
        for proc in process.children(recursive=True):
            proc.kill()
        process.kill()
        # self.driver_process.send_signal(signal.SIGINT)
        self.worker1_process.send_signal(signal.SIGINT)
        self.worker2_process.send_signal(signal.SIGINT)
        self.info("Benchmark safely ends", rela=self.start_time)
    
    def _openmsg_run_driver(self):
        cmd = ['bin/benchmark',
        f'--drivers driver-kafka/{self.benchmark.driver}.yaml',
        '--workers http://0.0.0.0:8082,http://0.0.0.0:8084',
        f'workloads/{self.benchmark.workload_file}.yaml']
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
    def _post_process(self):
        p = subprocess.run(['docker-compose', 'logs'], stdout=open(self.log.compose,'w'), stderr =subprocess.STDOUT, cwd=self.tool.compose)

# nw_fault = SlowFault(
#     type_="nw", # nw or fs
#     location_ = "kafka1", # e.g., datanode
#     duration_ = 10,
#     severity_ = "slow-low",
#     start_time_ = 5)
# fs_fault = SlowFault(
#     type_="fs", # nw or fs
#     location_ = "kafka1", # e.g., datanode
#     duration_ = 20,
#     severity_ = "10000",
#     start_time_ = 5)
# b = PERFTEST_KAFKA(exec_time_ = 30)
# # b = OPENMSG_KAFKA(exec_time_ = 30)

# t = Kafka(sys_name_= "kafka",
#                fault_ = fs_fault,
#                benchmark_= b,
#                data_dir_= "xixi1",
#                log_root_dir_='/users/YXXinda/workdir/data/default',
#                xinda_software_dir_="/users/YXXinda/workdir/xinda-software",
#                xinda_tools_dir_="/users/YXXinda/workdir/xinda/tools",
#                charybdefs_mount_dir_="/users/YXXinda/workdir/tmp")