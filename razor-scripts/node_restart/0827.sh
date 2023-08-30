###################### /data/ruiming/xinda/razor-scripts/node_restart/0827.sh ######################
## HBase + HDFS/ZooKeeper + YCSB
## Currently at least available on razor13
## bash /data/ruiming/xinda/razor-scripts/node_restart/0827.sh a 10000 3_ slow hbase-regionserver restart-slow6-dur5-0-5 slow6 1 setup1
## $1 a/b/c/d/e/f 
## $2 recordcount=10000 
## $3 operationcount 
## $4 fault_type = flaky/slow/normal
## $5 location = cas1, cas2
## $6 fault_name  e.g., restart-slow3-dur5-0-5, norestart-slow3-dur5-0-5
## $7 blockade_identifier e.g., slow1, slow2, flaky1 slow6(default)
## $8 iteration_identifier e.g., 1 2 3 4, ..., 100
## $9 setup_identifier e.g., setup1-full, setup-1st-half, setup3-2nd-half
function print_red_underlined() {
	echo -e "\e[4m\e[31m$1\e[0m"
}
set -m

function check_if_3_node_UN() {
	while [[ "$(docker exec -it cas1 nodetool status| grep 'UN ' | awk '{print $2}' | wc -l)" != 3 ]]; do
		print_red_underlined "Still waiting for cluster to set up. Sleep 10s"
		sleep 10
	done
	print_red_underlined "Cassandra cluster properly set up."
}

function create_dir_if_not_exist() {
    if [ ! -d $1 ]; then
        mkdir $1
        print_red_underlined "[$(date +%s%N), $(date +"%H:%M:%S")] Directory $1 created."
    else
        print_red_underlined "[$(date +%s%N), $(date +"%H:%M:%S")] Directory $1 already exists."
        #exit 1
    fi
}

data_dir=/data/ruiming/data/node_restart
ycsb_dir=/data/ruiming/xinda/softwares/ycsb-0.17.0
docker_compose_dir=/data/ruiming/xinda/razor-scripts/node_restart/docker-hbase-master
blockade_dir=/data/ruiming/xinda/razor-scripts/node_restart/blockade
running_pid_dir=/data/ruiming/xinda/razor-scripts/node_restart/get_running_pid.sh
init_hbase_dir=/data/ruiming/xinda/razor-scripts/node_restart/hbase-init.sh
check_pid_hbase_dir=/data/ruiming/xinda/razor-scripts/node_restart/hbase-check-pid.sh
running_pos=hbase-regionserver2
blockade_file=blockade-$7.yaml
cd $data_dir
log_dir1=hbase
log_dir2=${log_dir1}/$9
create_dir_if_not_exist $data_dir
create_dir_if_not_exist $log_dir1
create_dir_if_not_exist $log_dir2

cd ${data_dir}/${log_dir2}
if [ -e 1run-$5-$6-$8.log ]; then
	rm 1run-$5-$6-$8.log
fi
touch 1run-$5-$6-$8.log
rlog_pos=${data_dir}/${log_dir2}/1run-$5-$6-$8.log


echo "" >> $rlog_pos
echo "###################################" >> $rlog_pos
echo "[$(date +%s%N), $(date +"%H:%M:%S")] Current scheme is:" >> $rlog_pos
echo "Workload${1} with recordcount=${2} and operationcount=${3}" >> $rlog_pos
echo "Location: $5" >> $rlog_pos
echo "Fault type: $4" >> $rlog_pos

cd $docker_compose_dir
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Bringing up a new docker-compose cluster" >> $rlog_pos
nohup docker-compose up > ${data_dir}/${log_dir2}/compose-$5-$6-$8.log &
# check_if_3_node_UN
sleep 60
echo "[$(date +%s%N), $(date +"%H:%M:%S")] A new cluster is properly set up." >> $rlog_pos

region2_ip=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' hbase-regionserver2)
cd $blockade_dir
blockade --config $blockade_file up
blockade --config $blockade_file add hbase-master
blockade --config $blockade_file add hbase-regionserver
print_red_underlined "$running_pos IP: $region2_ip"

# preparing init_hbase.sh
# echo "# Initialize HBase" >> $init_hbase_dir
# echo "echo \"n_splits = 200; create 'usertable', 'family', {SPLITS => (1..n_splits).map {|i| \"user#{1000+i*(9999-1000)/n_splits}\"}}\" | ./opt/hbase-1.2.6/bin/hbase shell" >> $init_hbase_dir
# echo "# Load YCSB" >> $init_hbase_dir
# echo "/tmp/ycsb-0.17.0/bin/ycsb load hbase12 -s -P /tmp/ycsb-0.17.0/workloads/workload${1} -cp /etc/hbase -p recordcount=$2 -p columnfamily=family" >> $init_hbase_dir

# init
docker cp $init_hbase_dir ${running_pos}:/tmp/hbase-init.sh
docker cp $check_pid_hbase_dir ${running_pos}:/tmp/hbase-check-pid.sh
docker exec -it ${running_pos} bash /tmp/hbase-init.sh
echo "[$(date +%s%N), $(date +"%H:%M:%S")] TABLE:usertable COLUMNFAMILY:family initiated" >> $rlog_pos
docker cp $ycsb_dir ${running_pos}:/tmp/

# load YCSB wodkload
docker exec -it $running_pos /tmp/ycsb-0.17.0/bin/ycsb load hbase12 -s -P /tmp/ycsb-0.17.0/workloads/workload${1} -cp /etc/hbase -p recordcount=$2 -p columnfamily=family
echo "[$(date +%s%N), $(date +"%H:%M:%S")] ${ycsb_dir}/workloads/workload${1} successfully loaded" >> $rlog_pos
print_red_underlined "[$(date +%s%N), $(date +"%H:%M:%S")] ${ycsb_dir}/workloads/workload${1} successfully loaded"

start_time=$(date +%s)
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] $5-$6-$8 begins" >> $rlog_pos

# docker exec -it $running_pos /tmp/ycsb-0.17.0/bin/ycsb run hbase12 -s -P /tmp/ycsb-0.17.0/workloads/workload${1} -cp /etc/hbase -p measurementtype=raw -p operationcount=10000000 -p maxexecutiontime=150 -p status.interval=1 -p columnfamily=family > ${data_dir}/${log_dir2}/raw-$5-$6-$8.log & # 2> >(tee ${data_dir}/${log_dir2}/runtime-$5-$6-$8.log >&2) &

docker exec -d $running_pos sh -c "/tmp/ycsb-0.17.0/bin/ycsb run hbase12 -s -P /tmp/ycsb-0.17.0/workloads/workload${1} -cp /etc/hbase -p measurementtype=raw -p operationcount=10000000 -p maxexecutiontime=150 -p status.interval=1 -p columnfamily=family > /tmp/raw-$5-$6-$8.log 2> /tmp/runtime-$5-$6-$8.log"

echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Now wait 30s before cluster performance is stable " >> $rlog_pos
sleep 30
#################hahahah##############
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Sourcing $6 now" >> $rlog_pos
source /data/ruiming/data/node_restart/faults/${6}.sh
# docker restart cas1
# cd $blockade_dir
# blockade slow cas1
#################hahahah##############
docker exec -it $running_pos bash /tmp/hbase-check-pid.sh >> $rlog_pos
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Program safely ends" >> $rlog_pos

cd ${data_dir}/${log_dir2}
docker cp $running_pos:/tmp/raw-$5-$6-$8.log .
docker cp $running_pos:/tmp/runtime-$5-$6-$8.log .
cat raw-$5-$6-$8.log | grep -e "READ," -e "UPDATE," -e "SCAN," -e "INSERT," -e "READ-MODIFY-WRITE," > ts-$5-$6-$8.log
cat raw-$5-$6-$8.log | grep -v -e "READ," -e "UPDATE," -e "SCAN," -e "INSERT," -e "READ-MODIFY-WRITE," > sum-$5-$6-$8.log
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Convert raw to ts/sum" >> $rlog_pos

docker logs hbase-master > ${data_dir}/${log_dir2}/docker-$5-master-$6-$8.log
docker logs hbase-regionserver > ${data_dir}/${log_dir2}/docker-$5-regionserver-$6-$8.log
docker logs hbase-regionserver1 > ${data_dir}/${log_dir2}/docker-$5-regionserver1-$6-$8.log
docker logs hbase-regionserver2 > ${data_dir}/${log_dir2}/docker-$5-regionserver2-$6-$8.log

cd $docker_compose_dir
docker-compose down
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Docker-compose destroyed" >> $rlog_pos

echo "y" | docker volume prune

cd $blockade_dir
blockade --config $blockade_file destroy
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Blockade destroyed" >> $rlog_pos

echo "## [$(date +%s%N), $(date +"%H:%M:%S")] THE END" >> $rlog_pos
echo "" >> $rlog_pos
