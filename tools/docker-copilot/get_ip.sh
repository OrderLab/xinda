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
done