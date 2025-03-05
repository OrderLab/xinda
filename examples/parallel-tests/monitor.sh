#!/bin/bash

# List of all hosts
hosts=( $(cat ./hosts | awk '{print $1}') )
echo "Enter your CloudLab username"
read username
# check if path_to_xinda is empty
if [ -z "$username" ]; then
  echo "username is empty. Abort!"
  exit 0
fi

echo "Enter path to xinda on test nodes:"
read path_to_xinda
# check if path_to_xinda is empty
if [ -z "$path_to_xinda" ]; then
  echo "Path to xinda is empty. Abort!"
  exit 0
fi

mkdir -p logs

# Loop through each host
for i in "${!hosts[@]}"; do
    host=${hosts[$i]}
    echo -n "$host [$(($i+1))/${#hosts[@]}]"
    ssh ${username}@$host cat "$path_to_xinda/examples/*.log" > logs/${host}.log
    if ! grep -ie "error" -ie "exception" "logs/${host}.log"; then
        echo -n " [OK]"
    fi
    num_end=$(cat logs/${host}.log | grep END | wc -l)
    echo " [Done: "$num_end"]"
done