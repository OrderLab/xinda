docker network create -d bridge roachnet
docker volume create roach1
docker volume create roach2
docker volume create roach3

docker run -d --name=roach1 --hostname=roach1 --net=roachnet -p 26257:26257 -p 8080:8080 -v "roach1:/cockroach/cockroach-data" cockroachdb/cockroach:v23.1.11 start   --advertise-addr=roach1:26357   --http-addr=roach1:8080   --listen-addr=roach1:26357   --sql-addr=roach1:26257   --insecure   --join=roach1:26357,roach2:26357,roach3:26357

docker run -d   --name=roach2   --hostname=roach2   --net=roachnet   -p 26258:26258   -p 8081:8081   -v "roach2:/cockroach/cockroach-data"   cockroachdb/cockroach:v23.1.11 start     --advertise-addr=roach2:26357     --http-addr=roach2:8081     --listen-addr=roach2:26357     --sql-addr=roach2:26258     --insecure     --join=roach1:26357,roach2:26357,roach3:26357

docker run -d   --name=roach3   --hostname=roach3   --net=roachnet   -p 26259:26259   -p 8082:8082   -v "roach3:/cockroach/cockroach-data"   cockroachdb/cockroach:v23.1.11 start     --advertise-addr=roach3:26357     --http-addr=roach3:8082     --listen-addr=roach3:26357     --sql-addr=roach3:26259     --insecure     --join=roach1:26357,roach2:26357,roach3:26357

docker exec -it roach1 ./cockroach --host=roach1:26357 init --insecure
docker exec -it roach1 ./cockroach node status --host=roach1:26257 --insecure