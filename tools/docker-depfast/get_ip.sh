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

echo $ipServer1
echo $ipServer2
echo $ipServer3
echo $ipServer4
echo $ipServer5
echo $ipClient
