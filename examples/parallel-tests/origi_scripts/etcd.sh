echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 1 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 1 --unique_identifier 1 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 1 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 2 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 2 --unique_identifier 2 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 2 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 3 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 3 --unique_identifier 3 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 3 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 4 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 4 --unique_identifier 4 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 4 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 5 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 5 --unique_identifier 5 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 5 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 6 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 6 --unique_identifier 6 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 6 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 7 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 7 --unique_identifier 7 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 7 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 8 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 8 --unique_identifier 8 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 8 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 9 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 9 --unique_identifier 9 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 9 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 10 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 10 --unique_identifier 10 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 10 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 11 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 1 --unique_identifier 11 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 11 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 12 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 2 --unique_identifier 12 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 12 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 13 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 3 --unique_identifier 13 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 13 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 14 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 4 --unique_identifier 14 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 14 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 15 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 5 --unique_identifier 15 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 15 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 16 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 6 --unique_identifier 16 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 16 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 17 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 7 --unique_identifier 17 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 17 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 18 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 8 --unique_identifier 18 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 18 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 19 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 9 --unique_identifier 19 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 19 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 20 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-100us --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 10 --unique_identifier 20 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 20 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 21 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 1 --unique_identifier 21 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 21 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 22 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 2 --unique_identifier 22 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 22 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 23 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 3 --unique_identifier 23 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 23 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 24 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 4 --unique_identifier 24 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 24 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 25 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 5 --unique_identifier 25 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 25 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 26 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 6 --unique_identifier 26 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 26 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 27 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 7 --unique_identifier 27 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 27 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 28 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 8 --unique_identifier 28 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 28 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 29 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 9 --unique_identifier 29 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 29 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 30 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 10 --unique_identifier 30 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 30 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 31 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 1 --unique_identifier 31 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 31 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 32 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 2 --unique_identifier 32 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 32 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 33 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 3 --unique_identifier 33 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 33 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 34 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 4 --unique_identifier 34 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 34 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 35 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 5 --unique_identifier 35 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 35 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 36 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 6 --unique_identifier 36 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 36 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 37 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 7 --unique_identifier 37 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 37 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 38 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 8 --unique_identifier 38 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 38 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 39 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 9 --unique_identifier 39 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 39 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 40 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-1ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 10 --unique_identifier 40 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 40 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 41 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-10ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 1 --unique_identifier 41 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 41 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 42 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-10ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 2 --unique_identifier 42 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 42 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 43 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-10ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 3 --unique_identifier 43 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 43 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 44 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-10ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 4 --unique_identifier 44 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 44 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 45 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-10ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 5 --unique_identifier 45 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 45 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 46 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-10ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 6 --unique_identifier 46 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 46 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 47 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-10ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 7 --unique_identifier 47 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 47 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 48 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-10ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 8 --unique_identifier 48 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 48 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 49 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-10ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 9 --unique_identifier 49 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 49 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 50 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-10ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 10 --unique_identifier 50 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 50 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 51 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-10ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 1 --unique_identifier 51 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 51 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 52 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-10ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 2 --unique_identifier 52 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 52 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 53 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-10ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 3 --unique_identifier 53 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 53 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 54 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-10ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 4 --unique_identifier 54 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 54 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 55 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-10ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 5 --unique_identifier 55 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 55 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 56 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-10ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 6 --unique_identifier 56 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 56 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 57 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-10ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 7 --unique_identifier 57 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 57 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 58 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-10ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 8 --unique_identifier 58 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 58 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 59 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-10ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 9 --unique_identifier 59 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 59 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 60 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-10ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 10 --unique_identifier 60 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 60 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 61 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 1 --unique_identifier 61 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 61 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 62 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 2 --unique_identifier 62 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 62 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 63 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 3 --unique_identifier 63 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 63 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 64 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 4 --unique_identifier 64 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 64 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 65 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 5 --unique_identifier 65 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 65 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 66 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 6 --unique_identifier 66 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 66 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 67 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 7 --unique_identifier 67 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 67 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 68 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 8 --unique_identifier 68 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 68 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 69 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 9 --unique_identifier 69 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 69 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 70 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-100ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 10 --unique_identifier 70 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 70 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 71 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-100ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 1 --unique_identifier 71 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 71 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 72 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-100ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 2 --unique_identifier 72 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 72 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 73 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-100ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 3 --unique_identifier 73 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 73 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 74 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-100ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 4 --unique_identifier 74 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 74 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 75 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-100ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 5 --unique_identifier 75 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 75 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 76 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-100ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 6 --unique_identifier 76 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 76 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 77 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-100ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 7 --unique_identifier 77 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 77 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 78 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-100ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 8 --unique_identifier 78 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 78 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 79 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-100ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 9 --unique_identifier 79 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 79 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 80 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-100ms --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 10 --unique_identifier 80 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 80 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 81 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-1s --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 1 --unique_identifier 81 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 81 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 82 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-1s --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 2 --unique_identifier 82 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 82 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 83 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-1s --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 3 --unique_identifier 83 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 83 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 84 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-1s --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 4 --unique_identifier 84 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 84 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 85 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-1s --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 5 --unique_identifier 85 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 85 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 86 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-1s --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 6 --unique_identifier 86 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 86 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 87 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-1s --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 7 --unique_identifier 87 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 87 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 88 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-1s --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 8 --unique_identifier 88 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 88 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 89 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-1s --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 9 --unique_identifier 89 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 89 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 90 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity slow-1s --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 10 --unique_identifier 90 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 90 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 91 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-1s --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 1 --unique_identifier 91 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 91 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 92 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-1s --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 2 --unique_identifier 92 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 92 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 93 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-1s --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 3 --unique_identifier 93 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 93 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 94 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-1s --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 4 --unique_identifier 94 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 94 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 95 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-1s --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 5 --unique_identifier 95 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 95 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 96 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-1s --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 6 --unique_identifier 96 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 96 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 97 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-1s --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 7 --unique_identifier 97 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 97 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 98 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-1s --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 8 --unique_identifier 98 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 98 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 99 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-1s --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 9 --unique_identifier 99 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 99 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 100 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity slow-1s --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 10 --unique_identifier 100 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 100 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 101 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p1 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 1 --unique_identifier 101 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 101 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 102 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p1 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 2 --unique_identifier 102 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 102 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 103 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p1 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 3 --unique_identifier 103 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 103 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 104 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p1 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 4 --unique_identifier 104 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 104 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 105 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p1 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 5 --unique_identifier 105 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 105 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 106 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p1 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 6 --unique_identifier 106 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 106 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 107 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p1 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 7 --unique_identifier 107 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 107 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 108 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p1 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 8 --unique_identifier 108 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 108 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 109 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p1 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 9 --unique_identifier 109 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 109 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 110 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p1 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 10 --unique_identifier 110 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 110 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 111 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p1 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 1 --unique_identifier 111 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 111 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 112 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p1 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 2 --unique_identifier 112 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 112 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 113 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p1 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 3 --unique_identifier 113 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 113 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 114 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p1 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 4 --unique_identifier 114 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 114 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 115 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p1 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 5 --unique_identifier 115 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 115 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 116 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p1 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 6 --unique_identifier 116 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 116 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 117 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p1 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 7 --unique_identifier 117 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 117 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 118 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p1 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 8 --unique_identifier 118 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 118 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 119 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p1 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 9 --unique_identifier 119 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 119 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 120 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p1 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 10 --unique_identifier 120 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 120 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 121 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p10 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 1 --unique_identifier 121 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 121 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 122 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p10 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 2 --unique_identifier 122 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 122 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 123 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p10 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 3 --unique_identifier 123 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 123 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 124 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p10 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 4 --unique_identifier 124 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 124 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 125 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p10 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 5 --unique_identifier 125 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 125 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 126 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p10 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 6 --unique_identifier 126 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 126 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 127 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p10 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 7 --unique_identifier 127 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 127 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 128 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p10 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 8 --unique_identifier 128 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 128 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 129 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p10 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 9 --unique_identifier 129 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 129 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 130 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p10 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 10 --unique_identifier 130 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 130 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 131 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p10 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 1 --unique_identifier 131 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 131 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 132 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p10 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 2 --unique_identifier 132 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 132 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 133 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p10 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 3 --unique_identifier 133 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 133 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 134 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p10 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 4 --unique_identifier 134 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 134 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 135 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p10 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 5 --unique_identifier 135 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 135 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 136 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p10 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 6 --unique_identifier 136 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 136 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 137 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p10 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 7 --unique_identifier 137 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 137 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 138 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p10 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 8 --unique_identifier 138 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 138 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 139 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p10 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 9 --unique_identifier 139 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 139 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 140 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p10 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 10 --unique_identifier 140 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 140 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 141 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p40 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 1 --unique_identifier 141 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 141 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 142 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p40 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 2 --unique_identifier 142 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 142 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 143 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p40 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 3 --unique_identifier 143 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 143 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 144 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p40 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 4 --unique_identifier 144 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 144 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 145 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p40 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 5 --unique_identifier 145 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 145 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 146 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p40 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 6 --unique_identifier 146 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 146 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 147 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p40 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 7 --unique_identifier 147 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 147 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 148 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p40 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 8 --unique_identifier 148 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 148 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 149 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p40 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 9 --unique_identifier 149 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 149 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 150 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p40 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 10 --unique_identifier 150 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 150 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 151 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p40 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 1 --unique_identifier 151 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 151 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 152 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p40 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 2 --unique_identifier 152 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 152 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 153 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p40 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 3 --unique_identifier 153 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 153 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 154 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p40 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 4 --unique_identifier 154 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 154 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 155 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p40 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 5 --unique_identifier 155 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 155 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 156 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p40 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 6 --unique_identifier 156 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 156 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 157 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p40 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 7 --unique_identifier 157 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 157 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 158 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p40 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 8 --unique_identifier 158 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 158 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 159 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p40 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 9 --unique_identifier 159 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 159 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 160 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p40 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 10 --unique_identifier 160 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 160 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 161 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p70 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 1 --unique_identifier 161 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 161 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 162 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p70 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 2 --unique_identifier 162 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 162 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 163 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p70 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 3 --unique_identifier 163 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 163 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 164 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p70 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 4 --unique_identifier 164 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 164 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 165 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p70 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 5 --unique_identifier 165 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 165 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 166 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p70 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 6 --unique_identifier 166 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 166 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 167 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p70 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 7 --unique_identifier 167 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 167 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 168 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p70 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 8 --unique_identifier 168 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 168 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 169 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p70 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 9 --unique_identifier 169 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 169 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 170 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location leader --fault_duration 30 --fault_severity flaky-p70 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 10 --unique_identifier 170 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 170 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 171 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p70 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 1 --unique_identifier 171 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 171 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 172 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p70 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 2 --unique_identifier 172 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 172 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 173 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p70 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 3 --unique_identifier 173 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 173 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 174 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p70 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 4 --unique_identifier 174 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 174 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 175 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p70 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 5 --unique_identifier 175 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 175 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 176 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p70 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 6 --unique_identifier 176 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 176 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 177 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p70 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 7 --unique_identifier 177 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 177 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 178 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p70 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 8 --unique_identifier 178 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 178 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 179 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p70 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 9 --unique_identifier 179 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 179 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), BEGIN] 180 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
python3 /users/rmlu/workdir/xinda/main.py --sys_name etcd --data_dir sample_batch_test --fault_type nw --fault_location follower --fault_duration 30 --fault_severity flaky-p70 --fault_start_time 60 --bench_exec_time 150 --ycsb_wkl mixed --benchmark ycsb --iter 10 --unique_identifier 180 --batch_test_log /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo "## [$(date +%s%N), $(date +"%Y-%m-%d %H:%M:%S %Z utc%z"), END] 180 / 180" >> /users/rmlu/workdir/xinda/examples/meta-etcd.log
echo -e '\n' >> /users/rmlu/workdir/xinda/examples/meta-etcd.log

