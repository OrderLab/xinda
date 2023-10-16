


## Launch database & init replica set
```
./up.sh
```
## Shut down database & prune volume
```
./down.sh
```
## Check cluster node status
```
./status.sh
```
The database takes some time to initialize cluster nodes. If you check status immediately after `./up.sh`, it normally fails. Try again in a few seconds.
## Connect to sql
You can connect to sql of `roach_id` (from container `roach0` which serves as bystander outside the cluster):
```
./sql.sh [roach_id]
```
The following two commands are equivalent.
```
./sql.sh 2
docker exec -it roach0 ./cockroach sql --host=roach2:26257 --insecure
```

## DB operations
```
CREATE DATABASE bank;
CREATE TABLE bank.accounts (id INT PRIMARY KEY, balance DECIMAL);
INSERT INTO bank.accounts VALUES (1, 1000.50);
INSERT INTO bank.accounts VALUES (2, 2000.50);
SELECT * FROM bank.accounts;
DELETE FROM bank.accounts WHERE id = 2;
```

## Run workload
First load workload.
```
./ycsb.sh load
./sql.sh
SELECT COUNT(*) FROM ycsb.usertable;
```
Then run workload.
```
./ycsb.sh run
```

## References
[Start a multi-node cluster](https://www.cockroachlabs.com/docs/v23.1/start-a-local-cluster-in-docker-mac)

[cockroach workload](https://www.cockroachlabs.com/docs/stable/cockroach-workload)