#!/bin/bash

# List of all hosts
hosts=( $(cat ./hosts | awk '{print $1}') )
username="rmlu"
mkdir -p logs

# Loop through each host
for i in "${!hosts[@]}"; do
    host=${hosts[$i]}
    echo -n "$host [$(($i+1))/${#hosts[@]}] "
    ssh ${username}@$host du "-hs ~/workdir/data/*.tar | cut -f1"
done