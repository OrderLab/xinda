#!/bin/bash

# List of all hosts
hosts=( $(cat ./hosts | awk '{print $1}') )
username="rmlu"
mkdir -p logs
total_size=0

# Loop through each host
for i in "${!hosts[@]}"; do
    host=${hosts[$i]}
    echo -n "$host [$(($i+1))/${#hosts[@]}] "
    dsize=$(ssh ${username}@$host du "-hs ~/workdir/data/*.tar | cut -f1")
    echo $dsize
    total_size=$(echo "$total_size + $(echo $dsize | sed 's/[^0-9.]*//g')" | bc)
done

est_time_razor=$(printf "%.0f" $(echo "$total_size * 1024 / 2.2 / 60" | bc -l))
est_time_ring=$(printf "%.0f" $(echo "$total_size * 1024 / 30 / 60" | bc -l))
echo "Total size: ${total_size}G."
echo "To razor (2.2MB/s): ${est_time_razor}min"
echo "To ring  (30 MB/s): ${est_time_ring}min"