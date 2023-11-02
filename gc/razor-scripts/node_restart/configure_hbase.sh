REQUIRED_IMAGES=(bde2020/hadoop-namenode:2.0.0-hadoop2.7.4-java8 bde2020/hadoop-datanode:2.0.0-hadoop2.7.4-java8 bde2020/hadoop-resourcemanager:2.0.0-hadoop2.7.4-java8 bde2020/hadoop-nodemanager:2.0.0-hadoop2.7.4-java8 bde2020/hadoop-historyserver:2.0.0-hadoop2.7.4-java8 zookeeper:3.4.10 bde2020/hbase-master:1.0.0-hbase1.2.6 bde2020/hbase-regionserver:1.0.0-hbase1.2.6)
for IMAGE in ${REQUIRED_IMAGES[@]}; do
    docker pull $IMAGE
done

cd /data/ruiming/xinda/softwares
mv ycsb-0.17.0 ycsb-0.17.0-previous
tar -xvf ycsb-ruiming.tar
mv ycsb-ruiming ycsb-0.17.0


# # on razor
# SERVER_LIST=(razor14 razor15 razor16 razor17 razor19)
# for SERVER in ${SERVER_LIST[@]}; do
#     scp ycsb-ruiming.tar ruiming@${SERVER}:/data/ruiming/xinda/softwares/
# done
