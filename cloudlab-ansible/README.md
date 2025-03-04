# Usage Guide

## What does this do?

This folder contains `ansible` playbooks that can be used to configure any machines for `Xinda`. We use it to configure the nodes on CloudLab.

Specifically, below are the things that this folder do:

1. Installation
    - `docker` and `docker-compose`
    - `blockade`: installed in a conda environment with python3.6. The env is automatically activated when you login to the node.
    - `Thrift` and the correct toolchain to build it.
    - `Charybdefs` and the correct toolchain to build it: the `Charybdefs` source code is the modified version from the xinda-software repo. The built directory is copied to `~/charybdefs`.
2. Setup environment variables in `~/.bashrc`.
3. Clone Xinda and Xinda-software repos to `~/workdir`.

### Note

1. Most of the installed programs' binaries are either installed in or linked to `/usr/local/bin`. So even if you don't activate the conda environment, you can still use the `blockade` command.
2. Some of the environment variables might not be available in a non-interactive shell. Do mind that when you run the experiments (try to always use interactive shells).
3. **Important** This script is supposed to be run on a `c220g2` node (available in the wisconsin cluster). The `c220g2` node has a 480GB SATA SSD mounted at `/var/lib/docker`. The `workdir` is mounted on `/dev/sdb`, a 1.1TB HDD.

## How to use it?

### Step0: Create nodes on CloudLab

Create nodes on CloudLab with a `Ubuntu 18.04` profile by clicking Experiments -> Start Experiment.

### Step1: Setup ssh key forwarding

Execute the following command to start the ssh-agent on your local machine.

```bash
eval `ssh-agent -s`
```

Then you should add your private key that has access to the xinda and xinda-software repos to the agent.

```bash
ssh-add <path-to-private-key>
```

### Step2: Install ansible

We use Python==3.9.20 and pip==24.2 to install ansible in our local environment.

```bash
pip3 install ansible
ansible-playbook -h
```

### Step2: Create your `ansible_host` file

The `ansible_host` file is used to specify the hosts that you want to run the ansible-playbook on. The format of the file is as follows:

```bash
c220g2-011110.wisc.cloudlab.us ansible_connection=ssh ansible_user=YOUR_USERNAME ansible_port=22
```

You can add as many hosts as you want to the file. The `ansible_user` is the username that you use to login to the host. The `ansible_port` is the port that you use to ssh to the host. The `ansible_connection` is the connection type that you use to connect to the host. In our case, we use ssh.

### Step3: One-click setup using ansible-playbook

```bash
ansible-playbook -i ansible_host configure.yml
```

The `configure.yml` file is the playbook that runs all playbooks in this directory. You can also run individual playbooks by specifying the corresponding file name.

The setup process will take ~30 minutes to complete. The script will install all necessary dependencies for Xinda to deploy a distributed system, run benchmarks, inject slow faults, collect runtime logs and stats, and analyze the results. Once the setup is done, you can ssh into the remote machine and start using Xinda (by default, the code is located at `$HOME/workdir/xinda`).
