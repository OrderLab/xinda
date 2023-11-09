## exec_time sketch
Below is the estimated (sketch) execution time for each system per fault/benchmark setup.
| System | exec_time (min) |
| --- | --- |
| crdb | 3.5 |
| etcd | 3 |
| hadoop | 5 |
| cassandra | 7 |
| hbase | 4.5 |
| kafka | 3.3 |

## Comments
The total combination of experiment setups can be calculated as follows:
$$[fault\ type]\times[fault\ severity]\times[fault\ duration]\times[fault\ start\ time]\times[fault\ location]\times[Number\ of\ benchmarks/workloads]$$

For a full RQ1_1 test on crdb, we need to run
$$2\times10\times8\times1\times2\times12=3840,$$
which is really a 'nightmare': we need $3.5\times3840/60\approx224\ machine\ hours$, not to mention the time to analyze the results 🤔

> Iterating through all possible combinations of variables is indeed time-consuming. But we can't say for sure that these variables are not correlated: e.g., only some combinations could trigger a certain system behavior. I think the variable that is most easily excluded is $[fault\ location]$, as the nodes do not differ from each other in most distributed systems (except for hadoop and hbase). We can first try different values of $[fault\ location]$, make sure they won't affect results in some systems, and thus simplifying the equation step by step.

- [ ] Another thing is that we need to tune the parameters so that the system performance is reasonably good.

## Usage

```
python3 generate_test_script.py \
--sys_name <SYSNAME> \
--data_dir rq1_1 \
--start_time <LIST_OF_START_TIME> \
--duration <LIST_OF_DURATION> \
--fault_type <fs and/or nw>

# For example
python3 generate_test_script.py --sys_name crdb --data_dir rq1_1 --start_time 60 --duration -1 30  --fault_type fs nw

# A new bash script will be generated under this folder. To run the test script
bash crdb-fs-nw-dur--1-30.sh
```

