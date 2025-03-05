#!/bin/bash

# List of all hosts
hosts=( $(cat ./hosts | awk '{print $1}') )
username="rmlu"
# List of all scripts
# Help me get the absolute path of ls exp/*.job
scripts=( $(realpath exp/*.job | sort) )
# print number of scripts and hosts
echo "Number of scripts: ${#scripts[@]}"
echo "Number of hosts: ${#hosts[@]}"

echo "Do you want to proceed? (y/n)"
read ifcontinue
if [ "$ifcontinue" != "y" ]; then
  echo "Abort!"
  exit 0
fi

echo "Enter path to xinda on test nodes:"
read path_to_xinda
# check if path_to_xinda is empty
if [ -z "$path_to_xinda" ]; then
  echo "Path to xinda is empty. Abort!"
  exit 0
fi

# Loop through each host and script
for i in "${!scripts[@]}"; do
  host=${hosts[$i]}
  script=${scripts[$i]}

  # Skip if there are no more scripts
  if [ -z "$script" ]; then
    echo "No script for $host"
    continue
  fi

  # Set environment variable for script name
  export SCRIPT_NAME=$script

#  ansible_connection=ssh ansible_user=YXXinda ansible_port=22
  echo $host ansible_connection=ssh ansible_user=$username ansible_port=22 > ./tmp_host
  # Run ansible playbook for this host and script
  ansible-playbook -i ./tmp_host ../../cloudlab-ansible/run-script-in-tmux.yml --extra-vars "path_to_xinda=$path_to_xinda"
  echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z")] $script, $host" >> jobs_mapping.log
done
