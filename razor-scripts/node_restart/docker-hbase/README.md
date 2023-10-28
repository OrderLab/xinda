[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/big-data-europe/Lobby)

# misc (by ruiming)
```
# Check zookeeper connection status
docker exec -it zoo sh -c "echo srvr | nc zoo 2181"
docker exec -it zoo1 sh -c "echo srvr | nc zoo1 2181"
docker exec -it zoo2 sh -c "echo srvr | nc zoo2 2181"

docker exec -it zoo sh -c "echo stat | nc zoo 2181"
docker exec -it zoo1 sh -c "echo stat | nc zoo1 2181"
docker exec -it zoo2 sh -c "echo stat | nc zoo2 2181"

# Check zookeeper snapshot:
docker exec -it zoo ls /data/version-2
docker exec -it zoo1 ls /data/version-2
docker exec -it zoo2 ls /data/version-2

# Check zookeeper log:
docker exec -it zoo ls /datalog/version-2
docker exec -it zoo1 ls /datalog/version-2
docker exec -it zoo2 ls /datalog/version-2
```

If we use charybdefs to inject slow faults (--delay 1000000) to datanode and then create a new table in hbase, in datanode logs:
```
23/10/28 00:05:50 WARN datanode.DataNode: Slow BlockReceiver write data to disk cost:3102ms (threshold=300ms)
23/10/28 00:05:54 WARN datanode.DataNode: Slow flushOrSync took 4016ms (threshold=300ms), isSync:false, 
```
There will be exceptions too:
```
23/10/28 00:07:00 INFO datanode.DataNode: Receiving BP-859987769-172.30.0.11-1698451232857:blk_1073741850_1026 src: /172.30.0.2:54398 dest: /172.30.0.13:50010
23/10/28 00:07:03 WARN datanode.DataNode: Slow BlockReceiver write data to disk cost:4012ms (threshold=300ms)
23/10/28 00:07:08 WARN datanode.DataNode: Slow flushOrSync took 5001ms (threshold=300ms), isSync:false, flushTotalNanos=5001056653ns
23/10/28 00:07:29 INFO datanode.DataNode: Exception for BP-859987769-172.30.0.11-1698451232857:blk_1073741847_1023
java.io.IOException: Premature EOF from inputStream
	at org.apache.hadoop.io.IOUtils.readFully(IOUtils.java:202)
	at org.apache.hadoop.hdfs.protocol.datatransfer.PacketReceiver.doReadFully(PacketReceiver.java:213)
	at org.apache.hadoop.hdfs.protocol.datatransfer.PacketReceiver.doRead(PacketReceiver.java:134)
	at org.apache.hadoop.hdfs.protocol.datatransfer.PacketReceiver.receiveNextPacket(PacketReceiver.java:109)
	at org.apache.hadoop.hdfs.server.datanode.BlockReceiver.receivePacket(BlockReceiver.java:503)
	at org.apache.hadoop.hdfs.server.datanode.BlockReceiver.receiveBlock(BlockReceiver.java:903)
	at org.apache.hadoop.hdfs.server.datanode.DataXceiver.writeBlock(DataXceiver.java:805)
	at org.apache.hadoop.hdfs.protocol.datatransfer.Receiver.opWriteBlock(Receiver.java:137)
	at org.apache.hadoop.hdfs.protocol.datatransfer.Receiver.processOp(Receiver.java:74)
	at org.apache.hadoop.hdfs.server.datanode.DataXceiver.run(DataXceiver.java:253)
	at java.lang.Thread.run(Thread.java:748)
```
However, if we inject the same slow faults to namenode, the creation still takes super long time (in fact never finish) but both datanode/namenode logs do not have anything related to "slow"

# docker-hbase

# Standalone
To run standalone hbase:
```
docker-compose -f docker-compose-standalone.yml up -d
```
The deployment is the same as in [quickstart HBase documentation](https://hbase.apache.org/book.html#quickstart).
Can be used for testing/development, connected to Hadoop cluster.

# Local distributed
To run local distributed hbase:
```
docker-compose -f docker-compose-distributed-local.yml up -d
```

This deployment will start Zookeeper, HMaster and HRegionserver in separate containers.

# Distributed
To run distributed hbase on docker swarm see this [doc](./distributed/README.md):
