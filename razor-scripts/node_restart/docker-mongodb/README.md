


## Start up
To start a 3-node mongoDB cluster:
```
docker-compose up -d
docker ps -a
```
## Config
Then
```bash
docker exec -it mongodb1 bash
mongosh "mongodb://localhost:27017"
rs.initiate()
rs.add("mongodb2:27017")
rs.add("mongodb3:27017")
rs.status()

```

## DB operations
```
show dbs
db.mycoll.insert({name: "Max"})
db.mycoll.insertMany([{name: "Bob"}, {name:"Alex"}])
db.mycoll.find()
db.mycoll.replaceOne({"name": "Max"}, {"firstname": "Maxime", "surname": "Beugnet"})
db.mycoll.deleteOne({name: "Bob"})
db.mycoll.find({})
db.mycoll.deleteMany({})
db.mycoll.find({})
```

```
db.getMongo().setReadPref("primaryPreferred")
docker stop mongodb1
docker start mongodb1
```





## TODOs

* Write a bash script (say init.sh) to initialize the cluster. Something like this:

  ```bash
  docker exec -it mongodb1 bash
  echo "rs.initiate()" | mongosh "mongodb://localhost:27017" | exit
  echo "rs.add(\"mongodb2:27017\")" | mongosh "mongodb://localhost:27017" | exit
  echo "rs.add(\"mongodb3:27017\")" | mongosh "mongodb://localhost:27017" | exit
  echo "rs.add(\"mongodb4:27017\")" | mongosh "mongodb://localhost:27017" | exit
  ```

  Then `docker cp init.sh mongodb1:<some_directory>`  and `docker exec -it mongodb1 bash <some_directory>` will do.

* Use [YCSB-0.17.0](https://github.com/brianfrankcooper/YCSB/releases/tag/0.17.0) to test mongoDB. I think there would be many tutorials on this. Generally, we will first `load` the benchmark, and then `run` the benchmark. Here is some code I used to test Cassandra as a reference (some parameters -p could be different):
  ```
  # YCSB-load:
  ${ycsb_dir}/bin/ycsb.sh load cassandra-cql -p hosts=$cas1_ip -s -P ${ycsb_dir}/workloads/workload${1} -p recordcount=$2
  
  # YCSB-run:
  ${ycsb_dir}/bin/ycsb.sh run cassandra-cql -p hosts=$cas1_ip -s -P ${ycsb_dir}/workloads/workload${1} -p measurementtype=raw -p operationcount=$3 -p maxexecutiontime=150 -p status.interval=1 > ${data_dir}/${log_dir2}/raw-$5-$6-$8.log 2> >(tee ${data_dir}/${log_dir2}/runtime-$5-$6-$8.log >&2) &
  ```

  

