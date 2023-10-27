[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/big-data-europe/Lobby)

# Notes (by ruiming)
```
# Check zookeeper connection status
# Similar if we want to query zoo1 and zoo2
docker exec -it zoo sh -c "echo srvr | nc zoo 2181"
docker exec -it zoo sh -c "echo stat | nc zoo 2181"
```

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
