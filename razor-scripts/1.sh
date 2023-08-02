###################### ~/ycsb-my/faults-meeting4/1.sh ######################
## bash ~/ycsb-my/faults-meeting4/1.sh 
## $1 a/b/c/d/e/f 
## $2 recordcount=10000 
## $3 operationcount 
## $4 fault_type = flaky/slow/normal
## $5 location = cas1, cas2
## $6 fault_name  e.g., fault-1-1-freq1-slow1
print_red_underlined() {
    echo -e "\e[4m\e[31m$1\e[0m"
}
set -m
cas_block_loc=~/cas-block-single-seed.yaml
root_dir=~/ycsb-my/faults-meeting4
cd $root_dir
log_dir1=r${2}_o${3}
log_dir2=${log_dir1}/wkl${1}_logs
if [ ! -d $log_dir1 ]; then
	mkdir $log_dir1
	print_red_underlined "[$(date +%s%N), $(date +"%H:%M:%S")] Directory $log_dir1 urcecreated."
else
	print_red_underlined "[$(date +%s%N), $(date +"%H:%M:%S")] Directory $log_dir1 already exists."
	#exit 1
fi

if [ ! -d $log_dir2 ]; then
	mkdir $log_dir2
	print_red_underlined "[$(date +%s%N), $(date +"%H:%M:%S")] Directory $log_dir2 created."
else
	print_red_underlined "[$(date +%s%N), $(date +"%H:%M:%S")] Directory $log_dir2 already exists."
	#exit 1
fi

cd ${root_dir}/${log_dir2}
if [ -e 1run-$5-$6.log ]; then
	rm 1run-$5-$6.log
fi
touch 1run-$5-$6.log
rlog_pos=${root_dir}/${log_dir2}/1run-$5-$6.log

echo "" >> $rlog_pos
echo "###################################" >> $rlog_pos
echo "[$(date +%s%N), $(date +"%H:%M:%S")] Current scheme is:" >> $rlog_pos
echo "Workload${1} with recordcount=${2} and operationcount=${3}" >> $rlog_pos
echo "Location: $5" >> $rlog_pos
echo "Fault type: $4" >> $rlog_pos

cd ~

blockade --config $cas_block_loc join
blockade --config $cas_block_loc fast cas1
blockade --config $cas_block_loc fast cas2
~/cas/bin/cqlsh 172.17.0.2 9042 -f ~/ycsb-my/init.cql
echo "[$(date +%s%N), $(date +"%H:%M:%S")] KEYSPACE:ycsb and TABLE:usertable initiated" >> $rlog_pos
~/ycsb-0.17.0/bin/ycsb.sh load cassandra-cql -p hosts="172.17.0.2" -s -P ~/ycsb-0.17.0/workloads/workload${1} -p recordcount=$2
echo "[$(date +%s%N), $(date +"%H:%M:%S")] ~/ycsb-0.17.0/workloads/workload${1} successfully loaded" >> $rlog_pos
print_red_underlined "[$(date +%s%N), $(date +"%H:%M:%S")] ~/ycsb-0.17.0/workloads/workload${1} successfully loaded"

start_time=$(date +%s)
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] $5-$6 begins" >> $rlog_pos
~/ycsb-0.17.0/bin/ycsb.sh run cassandra-cql -p hosts="172.17.0.2" -s -P ~/ycsb-0.17.0/workloads/workload${1} -p measurementtype=raw -p operationcount=$3 -p maxexecutiontime=120 -p status.interval=1 > ${root_dir}/${log_dir2}/raw-$5-$6.log 2> >(tee ${root_dir}/${log_dir2}/runtime-$5-$6.log >&2) &
#################hahahah##############
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Sourcing $6 now" >> $rlog_pos
source ~/ycsb-my/faults-meeting4/faults/${6}.sh
#################hahahah##############
program_pid=$(bash ~/ycsb-my/get_running_pid.sh)
while ps -p $program_pid > /dev/null; do
	this_time=$(date +%s)
	print_red_underlined "Program $program_pid runs for $((this_time -start_time)) seconds."
	# Sleep for 1 second and increment the current time
	sleep 10
done
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Program safely ends" >> $rlog_pos

cd ${root_dir}/${log_dir2}
cat raw-$5-$6.log | grep -e "READ," -e "UPDATE," -e "SCAN," -e "INSERT," -e "READ-MODIFY-WRITE," > ts-$5-$6.log
cat raw-$5-$6.log | grep -v -e "READ," -e "UPDATE," -e "SCAN," -e "INSERT," -e "READ-MODIFY-WRITE," > sum-$5-$6.log
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Convert raw to ts/sum" >> $rlog_pos

docker cp cas1:/var/log/cassandra/debug.log  ${root_dir}/${log_dir2}/debug-$5-cas1-$6.log
docker cp cas2:/var/log/cassandra/debug.log  ${root_dir}/${log_dir2}/debug-$5-cas2-$6.log
docker cp cas3:/var/log/cassandra/debug.log  ${root_dir}/${log_dir2}/debug-$5-cas3-$6.log
mv ${root_dir}/${log_dir2}/debug-$5-$5-$6.log ${root_dir}/${log_dir2}/debug-$5-$5-$6-af-restart.log

cd ~
blockade destroy
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] Blockade destroyed, now bringing up" >> $rlog_pos

blockade --config $cas_block_loc up
check_ip_addr() {
	local nodetool_status=$(docker exec -it cas2 nodetool status)
	if echo "$nodetool_status" | grep -q "172\.17\.0\.4" && \
		echo "$nodetool_status" | grep -q "172\.17\.0\.3" && \
		echo "$nodetool_status" | grep -q "172\.17\.0\.2"; then
		print_red_underlined "All three IP addresses are present in the output."
		return 1
	else
		print_red_underlined "At least one IP address is missing from the output."
		return 0
	fi
}
while check_ip_addr; do
	print_red_underlined "Still waiting for cluster to set up. Sleep 10s"
	sleep 10
done
sleep 30
echo "[$(date +%s%N), $(date +"%H:%M:%S")] A new cluster is properly set up." >> $rlog_pos
echo "## [$(date +%s%N), $(date +"%H:%M:%S")] THE END" >> $rlog_pos
echo "" >> $rlog_pos

