###################### ~/ycsb-my/faults-meeting4/1.sh ######################
## bash ~/ycsb-my/faults-meeting4/1.sh 
## $1 a/b/c/d/e/f 
## $2 recordcount=10000 
## $3 operationcount 
## $4 fault_type = flaky/slow/normal
## $5 location = cas1, cas2
## $6 fault_name  e.g., fault-1-1-freq1-slow1
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
cd $data_dir
log_dir1=r${2}_o${3}
log_dir2=${log_dir1}/wkl${1}_logs
create_dir_if_not_exist $log_dir1
create_dir_if_not_exist $log_dir2

cd ${data_dir}/${log_dir2}
if [ -e 1run-$5-$6.log ]; then
	rm 1run-$5-$6.log
fi
touch 1run-$5-$6.log
rlog_pos=${data_dir}/${log_dir2}/1run-$5-$6.log


echo "" >> $rlog_pos
echo "###################################" >> $rlog_pos
echo "[$(date +%s%N), $(date +"%H:%M:%S")] Current scheme is:" >> $rlog_pos
echo "Workload${1} with recordcount=${2} and operationcount=${3}" >> $rlog_pos
echo "Location: $5" >> $rlog_pos
echo "Fault type: $4" >> $rlog_pos

cas1_ip=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' cas1)
cqlsh_dir=/data/ruiming/xinda/softwares/cas/bin/cqlsh
init_cql_dir=/data/ruiming/xinda/razor-scripts/init.cql
ycsb_dir=/data/ruiming/xinda/softwares/ycsb-0.17.0
docker_compose_dir=/data/ruiming/xinda/razor-scripts/docker
blockade_dir=/data/ruiming/xinda

cd docker_compose_dir
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Bringing up a new docker-compose cluster" >> $rlog_pos
nohup docker-compose up -f > ${data_dir}/${log_dir2}/compose-$5-$6.log &
check_if_3_node_UN

echo "[$(date +%s%N), $(date +"%H:%M:%S")] A new cluster is properly set up." >> $rlog_pos

cd $blockade_dir
blockade join
blockade fast cas1
blockade fast cas2
$cqlsh_dir $cas1_ip 9042 -f $init_cql_dir
echo "[$(date +%s%N), $(date +"%H:%M:%S")] KEYSPACE:ycsb and TABLE:usertable initiated" >> $rlog_pos
${ycsb_dir}/bin/ycsb.sh load cassandra-cql -p hosts=$cas1_ip -s -P ${ycsb_dir}/workloads/workload${1} -p recordcount=$2
echo "[$(date +%s%N), $(date +"%H:%M:%S")] ${ycsb_dir}/workloads/workload${1} successfully loaded" >> $rlog_pos
print_red_underlined "[$(date +%s%N), $(date +"%H:%M:%S")] ${ycsb_dir}/workloads/workload${1} successfully loaded"

start_time=$(date +%s)
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] $5-$6 begins" >> $rlog_pos
${ycsb_dir}/bin/ycsb.sh run cassandra-cql -p hosts=$cas1_ip -s -P ${ycsb_dir}/workloads/workload${1} -p measurementtype=raw -p operationcount=$3 -p maxexecutiontime=120 -p status.interval=1 > ${data_dir}/${log_dir2}/raw-$5-$6.log 2> >(tee ${data_dir}/${log_dir2}/runtime-$5-$6.log >&2) &
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Now wait 20s before cluster performance is stable " >> $rlog_pos
sleep 20
#################hahahah##############
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Sourcing $6 now" >> $rlog_pos
# source ~/ycsb-my/faults-meeting4/faults/${6}.sh
#################hahahah##############
program_pid=$(bash ~/ycsb-my/get_running_pid.sh)
while ps -p $program_pid > /dev/null; do
	this_time=$(date +%s)
	print_red_underlined "Program $program_pid runs for $((this_time -start_time)) seconds."
	# Sleep for 1 second and increment the current time
	sleep 10
done
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Program safely ends" >> $rlog_pos

cd ${data_dir}/${log_dir2}
cat raw-$5-$6.log | grep -e "READ," -e "UPDATE," -e "SCAN," -e "INSERT," -e "READ-MODIFY-WRITE," > ts-$5-$6.log
cat raw-$5-$6.log | grep -v -e "READ," -e "UPDATE," -e "SCAN," -e "INSERT," -e "READ-MODIFY-WRITE," > sum-$5-$6.log
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Convert raw to ts/sum" >> $rlog_pos

docker cp cas1:/var/log/cassandra/debug.log  ${data_dir}/${log_dir2}/debug-$5-cas1-$6.log
docker cp cas2:/var/log/cassandra/debug.log  ${data_dir}/${log_dir2}/debug-$5-cas2-$6.log
docker cp cas3:/var/log/cassandra/debug.log  ${data_dir}/${log_dir2}/debug-$5-cas3-$6.log
mv ${data_dir}/${log_dir2}/debug-$5-$5-$6.log ${data_dir}/${log_dir2}/debug-$5-$5-$6-af-restart.log

cd $blockade_dir
blockade destroy
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Blockade destroyed" >> $rlog_pos

cd $docker_compose_dir
docker-compose down
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Docker-compose destroyed" >> $rlog_pos
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] THE END" >> $rlog_pos
echo "" >> $rlog_pos
