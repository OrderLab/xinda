#!/bin/bash
getIPAddr() {
    docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $1
}
ipServer1=$(getIPAddr "server1")
ipServer2=$(getIPAddr "server2")
ipServer3=$(getIPAddr "server3")
ipServer4=$(getIPAddr "server4")
ipServer5=$(getIPAddr "server5")
ipClient=$(getIPAddr "client")

ip_list=($ipServer1 $ipServer2 $ipServer3 $ipServer4 $ipServer5 $ipClient)

node_list=(server1 server2 server3 server4 server5 client)

for i in "${!node_list[@]}"
do
	echo "${node_list[$i]}: ${ip_list[$i]}"
	docker exec -it ${node_list[$i]} service ssh start 1> /dev/null
done

for i in "${!node_list[@]}"
do
	for j in "${!ip_list[@]}"
	do
		if [ "$i" != "$j" ]; then
			docker exec -it ${node_list[$i]} bash -c "echo root | sshpass ssh-copy-id -f ${ip_list[$j]} 1> /dev/null"
		fi
	done
done

# docker exec -it client bash -c "./ip_config.sh $ipServer1 $ipServer2 $ipServer3 $ipServer4 $ipServer5 $ipClient"

for i in "${!node_list[@]}"
do
	docker exec -it ${node_list[$i]}  bash -c "./ip_config.sh $ipServer1 $ipServer2 $ipServer3 $ipServer4 $ipServer5 $ipClient"
	docker exec -it ${node_list[$i]}  bash -c "mkdir -p log; mkdir -p archive; mkdir -p tmp;"
	docker exec -it ${node_list[$i]}  bash -c "./init.sh"
done


#docker exec -it client bash -c "./batch_op.sh scp"
#docker exec -it client bash -c "./batch_op.sh dep"
#docker exec -it client bash -c "python3 waf configure -J build"
