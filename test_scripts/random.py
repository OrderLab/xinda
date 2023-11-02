import sys
sys.path.append('..')
from xinda.configs.slow_fault import SlowFault
from xinda.configs.benchmark import *
from xinda.systems import kafka
import os 
nw_fault = SlowFault(
    type_="nw", # nw or fs
    location_ = "cas1", # e.g., datanode
    duration_ = 30,
    severity_ = "slow3",
    start_time_ = 35)

print(nw_fault.info)

b = YCSB_CASSANDRA(exec_time_='150',workload_='a')
print(b.exec_time)


# nw_fault = SlowFault(
#     type_="nw", # nw or fs
#     location_ = "kafka1", # e.g., datanode
#     duration_ = 20,
#     severity_ = "slow3",
#     start_time_ = 35)
# fs_fault = SlowFault(
#     type_="fs", # nw or fs
#     location_ = "kafka1", # e.g., datanode
#     duration_ = 20,
#     severity_ = "10000",
#     start_time_ = 35)
# b = KAFKA()

# t = kafka.Kafka(sys_name_= "kafka",
#                fault_ = nw_fault,
#                benchmark_= b,
#                data_dir_= "xixi1")

print(os.path.dirname(os.path.abspath(__file__)))