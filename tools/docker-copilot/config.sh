#!/bin/bash
getIPAddr() {
    docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $1
}
ipControl=$(getIPAddr "control")
ipMaster=$(getIPAddr "master")
ipRep1=$(getIPAddr "replica1")
ipRep2=$(getIPAddr "replica2")
ipRep3=$(getIPAddr "replica3")
ipClient=$(getIPAddr "client")

ip_list=($ipControl $ipMaster $ipRep1 $ipRep2 $ipRep3 $ipClient)

node_list=(control master replica1 replica2 replica3 client)

for i in "${!node_list[@]}"
do
	echo "${node_list[$i]}: ${ip_list[$i]}"
	docker exec -it ${node_list[$i]} service ssh start 1> /dev/null
done

echo "Setting up ssh"
for i in "${!node_list[@]}"
do
    docker exec ${node_list[$i]} bash -c "cat ~/.ssh/id_rsa.pub" > ${node_list[$i]}.pub
	for j in "${!node_list[@]}"
	do
		if [ "$i" != "$j" ]; then
            echo "=== Configuring ${node_list[$i]}.pub on ${node_list[$j]}"
			# docker exec -it ${node_list[$i]} bash -c "echo root | sshpass ssh-copy-id -f ${ip_list[$j]} 1> /dev/null"
            docker cp ${node_list[$i]}.pub ${node_list[$j]}:/root > /dev/null
            docker exec -it ${node_list[$j]} bash -c "cat /root/${node_list[$i]}.pub >> /root/.ssh/authorized_keys"
		fi
	done
done


echo -e "\nConfiguring /root/.ssh/config and /etc/hosts"
for i in "${!ip_list[@]}"
do
    for j in "${!ip_list[@]}"
    do
	    docker exec -it ${node_list[$i]}  bash -c "sed -i 's/ip_of_${node_list[$j]}/${ip_list[$j]}/g' /root/.ssh/config"
        docker exec -it ${node_list[$i]}  bash -c "echo -e '${ip_list[$j]}\tnode-$j' >> /etc/hosts"
    done
    echo "=== Changed config on ${node_list[$i]}"
done

rm *.pub

./get_ip.sh