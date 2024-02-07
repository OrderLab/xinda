#!/bin/bash

# List of all hosts
hosts=( $(cat ./hosts | awk '{print $1}') )
username="rmlu"
mkdir -p logs

# Loop through each host
for i in "${!hosts[@]}"; do
    host=${hosts[$i]}
    echo "$host [$(($i+1))/${#hosts[@]}]"
    ssh ${username}@$host cat "~/workdir/xinda/test_scripts/RQ1_1/*.log" > logs/${host}.log
done