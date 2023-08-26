## bash /data/ruiming/xinda/razor-scripts/node_restart/0825.sh 1_ 2_ 3_ slow namenode restart-slow6-dur5-0-5 1 test
## $1 a/b/c/d/e/f 
## $2 recordcount=10000 
## $3 operationcount 
## $4 fault_type = flaky/slow/normal
## $5 location = namenode, datanode
## $6 fault_name  e.g., restart-slow3-dur5-0-5, norestart-slow3-dur5-0-5
## $7 blockade_identifier e.g., slow1, slow2, flaky1 slow6(default)
## $8 iteration_identifier e.g., 1 2 3 4, ..., 100
## $9 setup_identifier e.g., setup1-full, setup-1st-half, setup3-2nd-half
function print_red_underlined() {
	echo -e "\e[4m\e[31m$1\e[0m"
}
set -m

function check_if_3_node_UN() {
	while [[ "$(docker exec -it namenode hdfs dfsadmin -report | grep 'Live datanodes ' |grep -oP '\(.*\)' | tr -d '()')" != 3 ]]; do
		print_red_underlined "Still waiting for cluster to set up. Sleep 10s"
		sleep 10
	done
	while [[ "$(docker ps -a | grep '(healthy)' | wc -l)" != 9 ]]; do
		print_red_underlined "Still waiting for cluster to set up. Sleep 10s"
		sleep 10
	done
	print_red_underlined "Hadoop cluster properly set up."
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
docker_compose_dir=/data/ruiming/xinda/razor-scripts/node_restart/docker-hadoop-master
blockade_dir=/data/ruiming/xinda/razor-scripts/node_restart/blockade
blockade_file=blockade-$7.yaml
mrbench_dir=/opt/hadoop-3.2.1/share/hadoop/mapreduce/hadoop-mapreduce-client-jobclient-3.2.1-tests.jar

cd $data_dir
log_dir1=hadoop
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
echo "Location: $5" >> $rlog_pos

cd $docker_compose_dir
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Bringing up a new docker-compose cluster" >> $rlog_pos
nohup docker-compose up > ${data_dir}/${log_dir2}/compose-$5-$6-$8.log &
check_if_3_node_UN
echo "[$(date +%s%N), $(date +"%H:%M:%S")] A new cluster is properly set up." >> $rlog_pos
sleep 10

# cas1_ip=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' cas1)
cd $blockade_dir
blockade --config $blockade_file up
blockade --config $blockade_file add namenode
blockade --config $blockade_file add datanode
blockade --config $blockade_file add datanode1
blockade --config $blockade_file add datanode2
# print_red_underlined "cas1 IP: $cas1_ip"


start_time=$(date +%s)
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] $5-$6-$8 begins" >> $rlog_pos
####################################################################################################

function running_mrbench_iteratively() {
    # $1 iteration_ary
    # $2 = $5-$6-$8
	iteration_ary=$1
    for iter in ${iteration_ary[@]}; do
        echo "## [$(date +%s%N), $(date +"%H:%M:%S")] ${iter} begins /$(echo $iteration_ary | wc -w)" > ${data_dir}/${log_dir2}/raw-$2-mrbench${iter}.log
        docker exec -it namenode yarn jar $mrbench_dir mrbench -numRuns 10 > ${data_dir}/${log_dir2}/raw-$2-mrbench${iter}.log 2> >(tee ${data_dir}/${log_dir2}/runtime-$2-mrbench${iter}.log >&2)
        echo "## [$(date +%s%N), $(date +"%H:%M:%S")] ${iter} ends /$(echo $iteration_ary | wc -w)" > ${data_dir}/${log_dir2}/raw-$2-mrbench${iter}.log
    done
} 
iteration_ary=($(seq 1 10))
running_mrbench_iteratively $iteration_ary $5-$6-$8 &

# docker exec -it namenode yarn jar $mrbench_dir mrbench -numRuns 10   > ${data_dir}/${log_dir2}/raw-$5-$6-$8.log 2> >(tee ${data_dir}/${log_dir2}/runtime-$5-$6-$8.log >&2) &

echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Now wait 30s before cluster performance is stable " >> $rlog_pos
sleep 30
#################hahahah##############
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Sourcing $6 now" >> $rlog_pos
source /data/ruiming/data/node_restart/faults/${6}.sh
# docker restart cas1
# cd $blockade_dir
# blockade slow cas1
#################hahahah##############
last_mrbench_iter_fn=${data_dir}/${log_dir2}/raw-$2-mrbench${iteration_ary[-1]}.log
while [ -e "$last_mrbench_iter_fn" ] &&  cat $last_mrbench_iter_fn | grep -q "ends" ; do
	this_time=$(date +%s)
	print_red_underlined "$(echo $iteration_ary | wc -w) mrbench runs for $((this_time -start_time)) seconds."
	sleep 10
done
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Program safely ends" >> $rlog_pos

cd ${data_dir}/${log_dir2}

docker logs datanode > ${data_dir}/${log_dir2}/debug-$5-datanode-$6-$8.log
docker logs datanode1 > ${data_dir}/${log_dir2}/debug-$5-datanode1-$6-$8.log
docker logs namenode > ${data_dir}/${log_dir2}/debug-$5-namenode-$6-$8.log
# mv ${data_dir}/${log_dir2}/debug-$5-$5-$6-$8.log ${data_dir}/${log_dir2}/debug-$5-$5-$6-af-restart-$8.log

cd $docker_compose_dir
docker-compose down
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Docker-compose destroyed" >> $rlog_pos

cd $blockade_dir
blockade --config $blockade_file destroy
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Blockade destroyed" >> $rlog_pos

echo "y" | docker volume prune

echo "## [$(date +%s%N), $(date +"%H:%M:%S")] THE END" >> $rlog_pos
echo "" >> $rlog_pos
