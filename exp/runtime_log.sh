#!/bin/bash

# List of all hosts
hosts=( $(cat ./hosts | awk '{print $1}') )
username="rmlu"
mkdir -p logs

# Loop through each host
for i in "${!hosts[@]}"; do
    host=${hosts[$i]}
    echo -n "$host [$(($i+1))/${#hosts[@]}]"
    ssh ${username}@$host cat "~/workdir/xinda/test_scripts/RQ1_1/*.log" > logs/${host}.log
    if grep -iq "exception" "logs/${host}.log"; then
        echo -n " [EXCEPTION]"
    else
        echo -n " [OK]"
    fi
    num_lines=$(cat logs/${host}.log | wc -l)
    echo " [Done: $(($num_lines/3))]"
done