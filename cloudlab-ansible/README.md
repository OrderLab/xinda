# Usage Guide

## What does this do?

This folder contains `ansible` playbooks that can be used to configure any machines for `xinda`. We use it to configure the nodes on cloudlab.

Specifically, below are the things that this folder do:

1. Installation
    - `docker` and `docker-compose`
    - `blockade``: installed in a conda environment with python3.6. The env is automatically activated when you login to the node.
    - `Thrift` and the correct toolchain to build it.
    - `Charybdefs` and the correct toolchain to build it: the `Charybdefs` source code is the modified version from the xinda-software repo. The built directory is copied to `~/charybdefs`.
2. Clone Xinda and Xinda-software repos to `~/workdir`.
3. Setup environment variables in `~/.bashrc`.

### Note

1. Most of the installed programs' binaries are either installed in or linked to `/usr/local/bin`. So even if you don't activate the conda environment, you can still use the `blockade` command.
2. Some of the environment variables might not be available in a non-interactive shell. Do mind that when you run the experiments (try to always use interactive shells).

## How to use it?

### Step0: Create nodes on cloudlab

Create nodes on cloudlab with `Ubuntu 18.04` image. To do this, the failureDetection project has a `Ubuntu18` profile that you can use. You can also use other profiles as long as the image is `Ubuntu 18.04`.

### Step1: Setup ssh key forwarding

Execute the following command to start the ssh-agent

```bash
eval `ssh-agent -s`
```

Then you should add your private key that has access to the xinda and xinda-software repos to the agent.

```bash
ssh-add <path-to-private-key>
```

### Step2: Install ansible

```bash
pip install ansible
ansible-galaxy collection install ansible.posix
```

### Step2: Create your `ansible_hosts` file

The `ansible_hosts` file is used to specify the hosts that you want to run the ansible playbook on. The format of the file is as follows:

```bash
clnode147.clemson.cloudlab.us ansible_connection=ssh ansible_user=YXXinda ansible_port=22
clnode148.clemson.cloudlab.us ansible_connection=ssh ansible_user=YXXinda ansible_port=22
```

You can add as many hosts as you want to the file. The `ansible_user` is the username that you use to login to the host. The `ansible_port` is the port that you use to ssh to the host. The `ansible_connection` is the connection type that you use to connect to the host. In our case, we use ssh.

### Step3: Run the ansible playbook

```bash
ansible-playbook -i ansible_hosts configure.yml
```

The `configure.yml` file is the playbook that runs all playbooks in this directory. You can also run individual playbooks by specifying the corresponding file name.
