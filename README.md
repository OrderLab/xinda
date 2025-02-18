# Overview

This repo contains the source code of (1) Xinda, a slow-fault testing pipeline; and (2) ADR, a lightweight runtime slow-fault detection library. The following sections are for building and running Xinda. Please refer to `./adr` for more information on ADR.

- [Overview](#overview)
  - [Requirements](#requirements)
  - [Install and configure dependencies](#install-and-configure-dependencies)
  - [Usage](#usage)
    - [1. Configuring Xinda](#1-configuring-xinda)
      - [1.1 Experiment Configuration](#11-experiment-configuration)
      - [1.2 System Configuration](#12-system-configuration)
      - [1.3 Benchmark Configuration](#13-benchmark-configuration)
      - [1.4 Slow-Fault Configuration](#14-slow-fault-configuration)
    - [2. Results Analysis](#2-results-analysis)
  - [Examples](#examples)
  - [Publication](#publication)

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
* The analysis part of Xinda requires the following Python packages:
    - pandas (==2.2.2)
    - tqdm (==4.66.2)


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
Applying Xinda to a system involves two steps: (1) configuring Xinda arguments and running the test experiment using `main.py`; (2) analyzing the test results using `analyze/process.py`.




### 1. Configuring Xinda



There are a few arguments to configure Xinda in terms of the system under test, the benchmark used, and the slow faults injected. Below are the main arguments to configure Xinda. The rest of the arguments can be found in `main.py` and are for development purposes.

```bash
python3 main.py -h

# Xinda: A slow-fault testing pipeline for distributed systems.
# optional arguments:
# ...
```

To reset/clean up the working environment for next Xinda test:

```bash
python3 cleanup.py
```

#### 1.1 Experiment Configuration
| Field | Default<br>Value | Description |
| - | - | - |
| log_root_dir | $HOME/workdir/data/default | The root directory to store logs (data) |
| data_dir | REQUIRED | Name of the experiment. Results will be stored in $log_root_dir/$sys_name/$data_dir |
| bench_exec_time | 150 | Benchmark duration in seconds |
| iter | 1 | Label for repeated experiments |

#### 1.2 System Configuration
| Field | Default<br>Value | Description |
| - | - | - |
| sys_name | REQUIRED |  Name of the distributed systems to be tested |
| cpu_limit | None | The number of CPU cores allocated to each container instance |
| mem_limit | None | The size of memory allocated to each container instance |



#### 1.3 Benchmark Configuration
| Field | Default<br>Value | Description |
| - | - | - |
| benchmark | REQUIRED | Specify which benchmark to test the system |
| ycsb_wkl | mixed | Other options are available in $HOME/workdir/xinda-software/ycsb-workloads |
| openmsg_driver | kafka-latency | The yaml filename of openmsg kafka driver. Available options are listed in `xinda-software/openmessaging/driver-kafka` |
| openmsg_workload | simple-workload |  The yaml filename of openmsg workload. Available options are listed in `xinda-software/openmessaging/workloads` |
| sysbench_lua_scheme | oltp_write_only | The lua scheme to run sysbench workload on crdb |
| etcd_official_wkl |  lease-keepalive | The benchmark from etcd official benchmarking tool to test etcd |

#### 1.4 Slow-Fault Configuration
| Field | Default<br>Value | Description |
| - | - | - |
| fault_type | REQUIRED |  Types of slow faults to be injected. Can be {nw, fs, None} |
| fault_location | REQUIRED | Fault injection location. Available hostnames are listed in `./xinda/systems/container.yaml` |
| fault_duration | REQUIRED | Duration of the fault injection in seconds |
| fault_severity | REQUIRED | Severity of the fault injection. For network slow faults, available options are listed in `./tools/blockade` (e.g., flaky-p10 or slow-100ms). For filesystem delays, just pass the delay to be injected in us (e.g., 1000 for 1ms or 100000 for 100ms) |
| fault_start_time | REQUIRED | Inject slow faults at X seconds after the benchmark is running |

### 2. Results Analysis
By default each Xinda test will generate a directory in `$HOME/workdir/data/default/${data_dir}`. The directory contains system logs and runtime stats of the test. To analyze the results, you can use the following command:
```bash
python3 $HOME/workdir/xinda/analyze/process.py \
    --data_dir PATH_TO_DATA_DIR \
    --output_dir PATH_TO_OUTPUT_DIR
```
The script will generate a summary of the test results into `meta.csv` stored in the output directory. It will also parse runtime logs (e.g., fault injection timestamps) and stats (e.g., system throughput time series).

## Examples

Let's start by running a sample Xinda test in HBase. We will inject a 1ms network delay to the regionserver for 60s:
```bash
python3 main.py \
    --sys_name hbase \
    --log_root_dir $HOME/workdir/data/example \
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
Xinda will first start to set up an HBase cluster, wait till initialization finishes, and run the YCSB benchmark for 150s (--bench_exec_time). After 60s (--fault_start_time) of the benchmark, Xinda will inject the slow fault and then clear it after 60s (--fault_duration). After benchmark ends, Xinda will save system logs and runtime stats to $HOME/workdir/data/example/hbase/sample_test (--log_root_dir and --data_dir). Finally, Xinda will safely shutdown the cluster and do the cleanup.

Now, let's analyze the test results using `process.py`
```bash
python3 $HOME/workdir/xinda/analyze/process.py \
    --data_dir $HOME/workdir/data/example \
    --output_dir $HOME/workdir/parsed_results
```
The parsed results will be stored in `$HOME/workdir/parsed_results`.

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