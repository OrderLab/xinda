from parse.context import *
from parse.runtime_parser import *
from parse.raw_parser import *
from parse.info_parser import *
from parse.compose_parser import *

def test_compose_parser():
    path = "/data/yuxuan/sensitivity/default/kafka/rq1_1/openmsg-1-topic-1-partition-1kb/kafka-throughput/compose-kafka1-nw-flaky-p70-dur30-60-90-16.log"
    path = "/home/yunchi/yuxuan/sensitivity/default/etcd-3.5.10/rq1_1/ycsb-mixed/compose-follower-nw-flaky-p70-dur30-60-90-46.log"
    path = "/data/yuxuan/sensitivity/default/cassandra/rq1_1/ycsb-mixed/compose-cas1-nw-flaky-p70-dur30-60-90-49.log"
    path = "/data/yuxuan/sensitivity/default/hbase/rq1_1/ycsb-mixed/compose-hbase-regionserver-nw-flaky-p70-dur30-60-90-10.log"
    path = "/home/yunchi/yuxuan/sensitivity/default/crdb/rq1_1/ycsb-a/crlog-roach1-fs-100000-dur30-60-90-32.log/cockroach.log"
    path = "/home/yunchi/yuxuan/sensitivity/default/crdb/rq1_1/ycsb-a/crlog-roach1-nw-flaky-p70-dur30-60-90-47.log"
    parser = ComposeParser()
    df = parser.parse(path)
    print(df)
    
    
def test_info_parser():
    path = "/home/yunchi/yuxuan/sensitivity/default/hadoop-3.3.6/rq1_1/terasort/info-namenode-nw-flaky-p40-dur30-30-60-14.log"
    parser = InfoParser()
    df = parser.parse(path)
    print(df)


def test_raw_parser():
    path = "/home/yunchi/data/yunchi/xinda/default/hadoop/rq1_1/mrbench/raw-datanode-nw-slow-high-dur20-60-80-1-mrbench.log"
    parser = RawParser()
    df = parser.parse(path)
    print(df)


def test_runtime_parser():
    path = "/home/yunchi/data/xinda/default/cassandra/rq1_1/writeonly/runtime-cas1-fs-1000000-dur60-60-120-1.log"
    path = "/home/yunchi/data/xinda/default/crdb/rq1_1/a/runtime-roach1-fs-10000-dur60-60-120-1.log"
    path = "/home/yunchi/data/xinda/default/etcd/rq1_1/mixed/runtime-etcd1-nw-high-dur60-60-120-1.log"
    path = "/home/yunchi/data/xinda/default/hbase/rq1_1/readonly/runtime-hbase-regionserver-nw-low-dur40-60-100-1.log"
    path = "/home/yunchi/yuxuan/xinda/default/crdb/rq1_1/sysbench-oltp_delete/runtime-roach2-nw-flaky-high-dur30-60-90-1.log"
    path = "/home/yunchi/yuxuan/xinda/default/etcd/rq1_1/official-stm-isolation_ss-locker_stm/runtime-leader-fs-1000000-dur50-60-110-1.log"
    parser = RuntimeParser()
    df = parser.parse(path)
    print(df)


def test_context_parser():
    path = "/data/yuxuan/hadoop_rq_all_fs/default/hadoop-3.3.6/restart/mrbench/runtime-datanode-restart-fs-10000-dur10-60-70-1-mrbench1.log. Cannot parse context from filename"
    # path = "/home/yunchi/yuxuan/sensitivity/default/crdb/rq1_1/ycsb-a/crlog-roach1-fs-100000-dur30-60-90-32.log/cockroach.log"
    # path = "/home/yunchi/yuxuan/sensitivity/default/crdb/rq1_1/ycsb-a/crlog-roach1-nw-flaky-p70-dur30-60-90-47.log"
    t = get_trial_setup_context_from_path(path)
    print(t)


# test_compose_parser()
# test_info_parser()
# test_raw_parser()
# test_runtime_parser()
test_context_parser()