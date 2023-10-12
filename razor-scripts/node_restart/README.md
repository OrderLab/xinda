## Directories
* `./blockade/*` contains the blockade config files. To bring a blockade container up:
    * (:warning: You need to `docker pull luca3m/sleep` for the first time)
    * `blockade --config xxx.yaml up`
* `./docker-cassandra/*` contains the docker-compose file to bring up a 3-node Cassandra cluster
* `./docker-hadoop-master/*` contains the docker-compose file to bring up a 1-namenode, 3-datanode Hadoop cluster
* `./docker-hbase-master/*` contains the docker-compose file to bring up a 1-master, 3-regionserver HBase cluster, together with a 3-node ZooKeeper cluster and a simple 1-DN, 1NN Hadoop cluster
* `./faults/*` contains shell scripts to inject network-related slow faults using blockade, when running the distributed systems
* `./run_scripts/*` contains shell scripts to run experiments

## Files
* `0810-cassandra.sh`: bring up a 3-node Cassandra cluster and run YCSB workload for 150s **(:warning: need more exec time to observe residual effects)**
* `0825-mapreduce.sh`: bring up the Hadoop cluster and run 10 mrbench jobs iteratively (re-run if job failed)
* `0827-hbase.sh`: bring up the HBase cluster and run YCSB workload for 150s **(:warning: need more exec time to observe residual effects; need to change to load-run-load-run fashion)**
