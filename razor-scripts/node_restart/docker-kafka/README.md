# Xinda-Kafka

## Overview
This directory contains 
- one `docker-compose.yml` file that spins up a ***four-node*** Kakfa cluster in ***Kraft*** mode, and another container to run benchmarking scripts. 
- Kafka v3.5.0's source code which includes benchmarking tools (slightly adapted to our use case). Note that the code has been **compiled for Linux x86_64**. Recompile the project if Kafka is to be benchmarked on other platforms.

## Kafka Overview
Kafka is a distributed streaming platform. External applications (*producers*) produce messages and submit them to Kafka (*brokers*). These messages are then consumed by applications (*consumers*) that subscribed to the stream. 

In Kafka, an abstraction for message streams is `topic`. Producers send messages to a topic and consumers read messages from topics. A topic is characterized by:
- topic name
- maximal message size
- ***replication factor***: this factor specifies the number of replicas for the topic; **replicas are stored on different brokers (kafka nodes)**
- ***partitions***: this factor specifies the number of parititons for the topic; messages from different paritions are not dependent on each other (time-wise); **replication of paritions is controlled by replication factor**

A good way to understand partitions and replication factors is to think of *partitions* as vertical scaling, enabling parallel computation on one replica, and *replicas* as horizontal scaling.  

## Benchmarking Preparation
### Modify `docker_compose.yml`
The Kafka needs to be mounted into the benchmarking container. Please modify the docker compose manifest to reflect the real path.

### Topic Creation
To measure the performance of Kafka, we need to first create a topic. Execute the below command in the debug container `kafka-benchmarking`:
```bash
sh /kafka/bin/kafka-topics.sh \
	--create \
	--bootstrap-server kafka-1:9092 \
        --replication-factor <integer> \ # 4 as we have 4 kafka nodes
        --partitions <integer> \ # reasonable value would be from 1 to ~100 
	--topic test-xinda # name of the topic to be create
```

### Checking for Topic Replication and Partition Status
The command allows you to check the leader for each paritition and replica status (ISR stands for in-sync replicas).
```bash
sh /kafka/bin/kafka-topics.sh --bootstrap-server kafka-1:9092,kafka-2:9092,kafka-3:9092,kafka-4:9092 --describe --topic test-xinda 
```
Example output (topic was created with 3 partition and 4 replica):
```bash
Topic: test-xinda       TopicId: rosCO2PBRRWGZw7aTmQ4wQ PartitionCount: 3       ReplicationFactor: 4    Configs: 
        Topic: test-xinda       Partition: 0    Leader: 2       Replicas: 2,3,4,1       Isr: 2,3,4,1
        Topic: test-xinda       Partition: 1    Leader: 3       Replicas: 3,4,1,2       Isr: 3,4,1,2
        Topic: test-xinda       Partition: 2    Leader: 4       Replicas: 4,1,2,3       Isr: 4,1,2,3
```

### Checking for Kafka quorum status (membership of Kafka nodes, not the quorum of topics)
```bash
> sh /kafka/bin/kafka-metadata-quorum.sh --bootstrap-server kafka-1:9092 describe --status

ClusterId:              ZGI1NTk0YmY3NzVjNDk5MA
LeaderId:               4
LeaderEpoch:            2
HighWatermark:          2425
MaxFollowerLag:         0
MaxFollowerLagTimeMs:   370
CurrentVoters:          [1,2,3,4]
CurrentObservers:       []
```

```bash
> sh /kafka/bin/kafka-metadata-quorum.sh --bootstrap-server kafka-1:9092 describe --replication
NodeId  LogEndOffset    Lag     LastFetchTimestamp      LastCaughtUpTimestamp   Status  
4       2467            0       1697594204877           1697594204877           Leader  
1       2467            0       1697594204419           1697594204419           Follower
2       2467            0       1697594204419           1697594204419           Follower
3       2467            0       1697594204420           1697594204420           Follower
```

## Benchmarking
### Run producer performance test
```bash
sh /kafka/bin/kafka-producer-perf-test.sh \
	--topic test-xinda \
	--num-records <integer> \ # usually set to several millions to keep the consumer test run longer
	--producer-props bootstrap.servers=kafka-1:9092,kafka-2:9092,kafka-3:9092,kafka-4:9092 \ 
	--throughput -1 \ # -1 sets no limit on maximal throughput
	--record-size <number of bytes> \ # usually set to 1024 -- 1KB
	--reporting-interval 1000 # report every 1 second
```

### Run consumer performance test
```bash
sh /kafka/bin/kafka-consumer-perf-test.sh \
	--bootstrap-server kafka-1:9092,kafka-2:9092,kafka-3:9092,kafka-4:9092 \
	--messages 1000000 \ # number of messages to read
	--reporting-interval 1000 \
	--show-detailed-stats \ 
	--topic test-xinda \
	--timeout <milliseconds> # The maximum allowed time milliseconds between returned records. (default: 10000)  
```

The above two tests can be run together. Note that once producer perf tests have been run to generate messages in the topic. Consumer perf tests can be ran multiple times by reusing existing data in the topic. The default time for Kafka to delete consumed data is 7 days, but it can be configured to be shorter.

## Delete topics (in case disk space full)
```bash
sh /kafka/bin/kafka-topics.sh --bootstrap-server kafka-1:9092 --delete --topic test-xinda
```

### Run e2e latency measuring test
```bash
sh /kafka/bin/kafka-e2e-latency.sh \
	kafka-1:9092,kafka-2:9092,kafka-3:9092,kafka-4:9092 \
	<number of messages> \
	<1/all for producer acks> \ # producer proceeds only when 1 or all in-sync replicas have received the message 
	<size of each message>
```
Note that this test requires synchronous behavior between producer and consumer, thus it might not simulate a real world workload well, and also it does not support report-by-interval (can be implemented with a timer thread probably but I am not very familiar with JAVA)




