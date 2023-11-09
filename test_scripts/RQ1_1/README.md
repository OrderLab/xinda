## Usage

```
python3 generate_test_script.py --sys_name <SYSNAME> --data_dir rq1_1 --start_time <LIST_OF_START_TIME> --duration <LIST_OF_DURATION> --fault_type <fs and/or nw>

# For example
python3 generate_test_script.py --sys_name crdb --data_dir rq1_1 --start_time 60 --duration -1 30  --fault_type fs nw
python3 generate_test_script.py --sys_name cassandra --data_dir rq1_1 --start_time 60 --duration -1 5 10 20 30 40 50 60  --fault_type fs
```
