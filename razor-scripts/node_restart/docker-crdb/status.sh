roach_id=${1:-1}
docker exec -it roach0 ./cockroach node status --host=roach$roach_id:26257 --insecure
