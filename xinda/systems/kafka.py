from xinda.systems.TestSystem import *

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
        # create a test kafka topic
        self.init_kafka()
        # run basic-benchmark:consumer first
        self.basic_consumer()
        # then run basic-benchmark:producer
        self.basic_producer()
        self.start_time = int(time.time()*1e9)
        '''
        Currently, since the workload is heavy (50%+ cpu consumed), blockade cmds will take ~25s to finish
        '''
        self.inject()
        # wrap-up and end
        self._wait_till_benchmark_ends()
        self.docker_down()
        if self.fault.type == 'nw':
            self.blockade_down()
        elif self.fault.type == 'fs':
            self.charybdefs_down()
        self.info("THE END")
    
    def init_kafka(self):
        cmd = f"docker cp {self.tool.kafka} kafka-benchmarking:/"
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
        cmd = 'docker exec kafka-benchmarking sh /kafka/bin/kafka-producer-perf-test.sh --topic test-xinda --num-records 14000000 --producer-props bootstrap.servers=kafka1:9092,kafka2:9092,kafka3:9092,kafka4:9092 --throughput -1 --record-size 1024 --reporting-interval 1000' # report every 1 second
        # --num-records 1500000 + --throughput 10000
        # --num-records 14000000 + --throughput -1
        # 14M records will run in ~150s, taking up 54GB disk space
        # If we set scheduled cleanups at given frequency (see docker-compose.yml), the runtime performance will be affected (100 MB/s => < 10MB/s) and thus not worth it. So, make sure that the home directory has >60GB disk space.
        self.info("[PRODUCER] kafka-producer-perf-test.sh started", rela=self.start_time)
        self.producer_process = subprocess.Popen(cmd, shell=True, stdout=open(self.log.kafka_producer, 'a'), stderr=subprocess.DEVNULL)
    
    def basic_consumer(self):
        cmd = 'docker exec kafka-benchmarking sh /kafka/bin/kafka-consumer-perf-test.sh --bootstrap-server kafka1:9092,kafka2:9092,kafka3:9092,kafka4:9092 --messages 1500000  -reporting-interval 1000 --show-detailed-stats --topic test-xinda --timeout 10000'
        self.info("[CONSUMER] kafka-consumer-perf-test.sh started", rela=self.start_time)
        self.consumer_process = subprocess.Popen(cmd, shell=True, stdout=open(self.log.kafka_consumer, 'a'), stderr=subprocess.DEVNULL)
        ## docker exec -it kafka-benchmarking sh /kafka/bin/kafka-topics.sh --bootstrap-server kafka1:9092,kafka2:9092,kafka3:9092,kafka4:9092 --describe --topic test-xinda
        ## docker exec -it kafka-benchmarking sh /kafka/bin/kafka-metadata-quorum.sh --bootstrap-server kafka1:9092 describe --replication
    
    # def inject(self):
    #     self.inject_thread = threading.Thread(target=super().inject)
    #     self.inject_thread.start()
    
    def _wait_till_benchmark_ends(self):
        self.producer_process.poll()
        cur_time = self.get_current_ts()
        if cur_time < 150 and self.producer_process.returncode != 0:
            self.info(f"Sleep {150 - cur_time}s till the end", rela=self.start_time)
            time.sleep(150 - cur_time)
        self.producer_process.terminate()
        self.info("Benchmark safely ends", rela=self.start_time)


# nw_fault = SlowFault(
#     type_="nw", # nw or fs
#     location_ = "kafka1", # e.g., datanode
#     duration_ = 20,
#     severity_ = "slow3",
#     start_time_ = 35)
# fs_fault = SlowFault(
#     type_="fs", # nw or fs
#     location_ = "kafka1", # e.g., datanode
#     duration_ = 20,
#     severity_ = "10000",
#     start_time_ = 35)
# b = KAFKA()

# t = Kafka(sys_name_= "kafka",
#                fault_ = fs_fault,
#                benchmark_= b,
#                data_dir_= "xixi1")