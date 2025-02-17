# Overview

This repo contains the source code of (1) Xinda, a slow-fault injection
pipeline; and (2) ADR, a lightweight runtime slow-fault detection library. The following sections are for building and running Xinda. Please refer to `./adr` for more information on ADR.

## Requirements

* OS: Xinda is developed and deployed under **Ubuntu 18.04**.
* Hardware:
    - The basic workflow of Xinda described in this README can be done in just one single node.
    - Our experiment node uses the [CloudLab c220g2](https://docs.cloudlab.us/hardware.html#%28part._cloudlab-wisconsin%29) node type, which has two
    Intel E5-2660 v3 10-core CPUs at 2.60 GHz, 160GB ECC DDR4 2133 MHz memory, 
    and a 480GB Intel DC SATA SSD plus two 1.2TB 10K RPM 6G SAS HDDs for storage.
* Xinda leverages two fault injection tools. Here are the exact environment to build:
    - Python (==3.6.13)
    - Blockade (==0.4.0, for injecting network-related slow faults)
    - CharybdeFS for injecting filesystem-related slow faults:
        - CMake (==3.23.0)
        - Thrift (==0.10.0)
        - M4 (==1.4.19)
        - Autoconf (==2.69)
* Xinda maintains a separate repo, [xinda-software](https://github.com/OrderLab/xinda-software/tree/master), to build and configure cloud benchmarks (YCSB and OpenMessaging) and other utilities (docker-compose).


## Install and configure dependencies
Below we show how to configure Xinda on a remote CloudLab c220g2 machine. We use Ansible to automate the process.

First, let's install Ansible on your local machine. We use Python==3.9.20 and pip==24.2 to install Ansible in our local environment.
```bash
pip3 install ansible
ansible-playbook -h
```

<details>
  <summary>To allow Ansible to access and configure the remote machine, we need to set up SSH agent forwarding.</summary>

```bash
mkdir -p $HOME/.ssh
ssh_pid_file="$HOME/.ssh/ssh-agent.pid"
SSH_AUTH_SOCK="$HOME/.ssh/ssh-agent.sock"
if [ -z "$SSH_AGENT_PID" ]
then
        # no PID exported, try to get it from pidfile
        SSH_AGENT_PID=$(cat "$ssh_pid_file")
fi

if ! kill -0 $SSH_AGENT_PID &> /dev/null
then
        # the agent is not running, start it
        rm "$SSH_AUTH_SOCK" &> /dev/null
        >&2 echo "INFO [ssh-agent] Starting SSH agent, since it's not running; this can take a moment"
        eval "$(ssh-agent -s -a "$SSH_AUTH_SOCK")"
        echo "$SSH_AGENT_PID" > "$ssh_pid_file"
        ssh-add -A 2>/dev/null

        >&2 echo "INFO [ssh-agent] Started ssh-agent with '$SSH_AUTH_SOCK'"
else
        >&2 echo "INFO [ssh-agent] ssh-agent already on '$SSH_AUTH_SOCK' ($SSH_AGENT_PID)"
fi
export SSH_AGENT_PID
export SSH_AUTH_SOCK
ssh-add
```

</details>


Next, we need to configure the host file for Ansible to access the remote machine. We provide an example of the host file in `./cloudlab-ansible/ansible_host`. You need to modify the hostname, username, and port number to match your remote machine. Once set, we can set up the remote machine in one click using the following command:
```bash
# cd ./cloudlab-ansible/
ansible-playbook -i ansible_host configure.yml
```
The setup process will take ~30 minutes to complete. The script will install all necessary dependencies for Xinda to deploy a distributed system, run benchmarks, inject slow faults, collect runtime logs and stats, and analyze the results. Once the setup is done, you can ssh into the remote machine and start using Xinda (by default, the code is located at `$HOME/workdir/xinda`).

## Usage
The main script for running Xinda is `main.py`.


To reset/clean up the working environment for next Xinda test:

```bash
python3 cleanup.py
```

To run a sample Xinda test:
```bash
# Results will be saved to $HOME/workdir/data/sample_test
python3 main.py \
    --sys_name hbase \
    --data_dir sample_test \
    --fault_type nw \
    --fault_location hbase-regionserver \
    --fault_duration 60 \
    --fault_severity slow-1ms \
    --fault_start_time 60 \
    --bench_exec_time 150 \
    --ycsb_wkl mixed \
    --benchmark ycsb \
    --iter 1
```
## Publication
```bibtex
@inproceedings{SlowFaultStudy2025NSDI,
  author = {Lu, Ruiming and Lu, Yunchi and Jiang, Yuxuan and Xue, Guangtao and Huang, Peng},
  title = {One-Size-Fits-None: Understanding and Enhancing Slow-Fault Tolerance in Modern Distributed Systems},
  booktitle = {Proceedings of the 22nd USENIX Symposium on Networked Systems Design and Implementation},
  series = {NSDI '25},
  month = {April},
  year = {2025},
  location = {Philadelphia, PA, USA},
}
```