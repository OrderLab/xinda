1. add in docker-compose:
```
volumes:
    - ../jacoco:/jacoco
```
2. export javaagent to hadoop-env.sh in container
```
echo export HADOOP_OPTS=\"-javaagent:/jacoco/lib/jacocoagent.jar=destfile=/jacoco/data/out.exec,classdumpdir=/jacoco/data/dump -Djacoco-agent.attach=true \$HADOOP_OPTS\" >> /etc/hadoop/hadoop-env.sh
```
3. restart container (eg. datanode)
```
docker restart datanode
```
4. enter datanode container and output report (eg. classfile=mapreduce)
```
java -jar /jacoco/lib/jacococli.jar report /jacoco/data/out.exec --classfiles /opt/hadoop-3.2.1/share/hadoop/mapreduce --html /jacoco/reports/mapreduce
```
5. download the report folder to local