docker-compose up -d
docker exec -it kafka-1 chmod 777 -R /bitnami
docker exec -it kafka-2 chmod 777 -R /bitnami
docker exec -it kafka-3 chmod 777 -R /bitnami
docker exec -it kafka-4 chmod 777 -R /bitnami
