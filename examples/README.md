# Usage Guide

Welcome to the `examples` folder! This folder contains helper scripts of how to test a distributed system with `Xinda`, from Minimal Working Examples (MWEs) to more complex ones that run in parallel. It is assumed that you have already set up the environment on your test nodes (recommended using `ansible-playbook` on CloudLab c220g2 nodes as described [here](../cloudlab-ansible/README.md))

## Minimal Working Example (MWE)

The [minimal-working-examples](./minimal-working-examples/) folder contains basic scripts to run a simple Xinda test on all supported distributed systems, **with a single fault injection**. By changing slow-fault-related (e.g., `fault_severity`, `fault_location`, etc.) and benchmark-related (e.g., `ycsb_wkl`, `benchmark`, `openmsg_driver`, etc.) flags, you can easily test different fault scenarios.


## Xinda Tests in Parallel

The [parallel-tests](./parallel-tests/) folder contains scripts to run batch Xinda tests in parallel. Below we use `etcd` as an example, evaluating how diverse fault configurations ($\S$ 3.1 in our [paper](../docs/SlowFaultStudy2025NSDI.pdf)) and resource limits ($\S$ 3.2) affect its slow-fault tolerance. We also showcase how to measure the danger zone ($\S$ 3.3) of `etcd`, where a small increase in slow-fault severity leads to a significant increase in performance degradation.

### Step 1: Generate Batched Test Scripts

We use [`generate.py`](./parallel-tests/generate.py) to generate all possible Xinda configurations of `etcd` under diverse slow faults ($\S$ 3.1) and save them to a file. 

```bash
python3 generate.py \
    --sys_name etcd \
    --data_dir sample_batch_test \
    --path_to_xinda /users/USERNAME/workdir/xinda \
    --fault_type nw \
    --start_time 60 \
    --duration 30 \
    --unique_benchmark ycsb \
    --iter 10 \
    --scheme sensitivity
```

The `--path_to_xinda` flag specifies the path to the Xinda repo on your **test** nodes. The `--scheme` also accepts other test schemes, like `--scheme resource-limits` ($\S$ 3.2) and `--scheme danger-zone` ($\S$ 3.3). 

<details>
<summary> The generated scripts will be saved as ./parallel-tests/scripts/etcd.sh. </summary>

Despite commands to invoke Xinda (`main.py`), there are also wrappers to log the start and end time of each test into a meta log (`--batch_test_log`):
```bash
$ head scripts/etcd.sh

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 1 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 1 --unique_identifier 1 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 1 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

...
```

</details>

There are 180 Xinda tests in total: 9 severity levels $\times$ 2 locations $\times$ 10 iterations $\times$ 1 workload (YCSB mixed). To change this combination based on your needs, you should directly modify the `generate.py` script. For example, if you also want to incorporate YCSB-writeonly and YCSB-readonly workloads, you should modify the `self.ycsb_wkl` variable:
```python
# ./parallel-tests/generate.py
def __init__(...):
    ...
    # self.ycsb_wkl = ['mixed']
    self.ycsb_wkl = ['mixed', 'writeonly', 'readonly']
    ...
```

### Step 2: Split
First of all, we need to register the test nodes in the [`hosts`](./parallel-tests/hosts) file. Remember to fill in the hostnames and your CloudLab username.
```bash
c220g2-011310.wisc.cloudlab.us ansible_connection=ssh ansible_user=YOUR_USERNAME ansible_port=22 
...
```

Then, we use [`load_balance.py`](./parallel-tests/load_balance.py) to split the batched test scripts generated in Step 1 into multiple jobs for each test node. It will cut the `etcd.sh` script into multiple parts in-place and assign them to different job files. 

```bash
# Only print the assignment
$ python3 load_balance.py

# Assign jobs to each node and save to ./exp
$ python3 load_balance.py --generate
```
The script will also output the assignment to the console, including an estimated completion time for each node. The completion time is calculated based on a rough estimation of each test's runtime when `--bench_exec_time` is set to be 150s. This can be changed by tuning the `estimated_time` variable in [`load_balance.py`](./parallel-tests/load_balance.py).

The output will be similar to the following:
```log
## Task Summary (3 nodes)
{'etcd': {'time': 3, 'count': 180}}

## Schedule
Node 1: {'etcd': 60}, Total time: 180min / 3.00hr / 03-05 15:38 -> 03-05 18:38
Node 2: {'etcd': 60}, Total time: 180min / 3.00hr / 03-05 15:38 -> 03-05 18:38
Node 3: {'etcd': 60}, Total time: 180min / 3.00hr / 03-05 15:38 -> 03-05 18:38
...
```

### Step 3: Distribute
Lastly, we use [`distribute_scripts.sh`](./parallel-tests/distribute_scripts.sh) to distribute and execute the job files. It will first upload job files to test nodes using `scp`, and then execute them in a remote `tmux` session using `ansible-playbook`. 

**(Important)** The script will prompt you to confirm the number of scripts and hosts, and ask for the path to the Xinda repo on the test nodes.

```bash
$ ./distribute_scripts.sh

Number of scripts: 3
Number of hosts: 3
Do you want to proceed? (y/n): y

Enter path to xinda on test nodes: /users/USERNAME/workdir/xinda

# Iteratively upload & execute job files on each test node with ansible
PLAY [all] *******
TASK [Gathering Facts] *******
```

### Step 4: Monitor (Optional)
You can use the [`monitor.sh`](./parallel-tests/monitor.sh) script to check the progress on each node.

**(Important)** The script will prompt you for your username on CloudLab and the path to the Xinda repo on the test nodes.
```bash
$ ./monitor.sh

Enter your CloudLab username: YOUR_USERNAME

Enter path to xinda on test nodes: /users/USERNAME/workdir/xinda

c220g2-011310.wisc.cloudlab.us [1/3] [OK] [Done: 3]
c220g2-011003.wisc.cloudlab.us [2/3] [OK] [Done: 2]
c220g2-011309.wisc.cloudlab.us [3/3] [OK] [Done: 1]
```

The `tmux` session created in Step 3 is split into 2 panes, one for the job execution and the other for monitoring the progress. To log onto a specific node and check progress:

```bash
ssh USERNAME@HOSTNAME
tmux a -t xinda_exp
```

### Step 5: Collect Results
After all tests are done, you can use our [analysis scripts](../data-analysis/process.py) to parse the results. After it finishes, you can use the [compress_exp_data.yml](../cloudlab-ansible/compress_exp_data.yml) playbook to compress the results on each node into a .tar archive. 

(**Important**) Remember to double-check the path to the parsed results in `compress_exp_data.yml` and also pass the `task` variable to specify the task name. After tat, you can download the compressed results to a persistent storage for further analysis.

```bash
# cd path_to_xinda/examples/parallel-tests
ansible-playbook -i hosts ../../cloudlab-ansible/compress_exp_data.yml --extra-vars "task=TASK_NAME"
```
