


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

# Or alternatively
docker exec -it mongodb1 bash
echo "rs.initiate()" | mongosh "mongodb://localhost:27017" | exit
echo "rs.add(\"mongodb2:27017\")" | mongosh "mongodb://localhost:27017" | exit
echo "rs.add(\"mongodb3:27017\")" | mongosh "mongodb://localhost:27017" | exit
echo "rs.add(\"mongodb4:27017\")" | mongosh "mongodb://localhost:27017" | exit
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