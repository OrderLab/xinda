from parse.raw_parser import *
def test_raw_parser():
    path = "/home/yunchi/data/xinda/default/hadoop/rq1_1/mrbench/raw-namenode-nw-high-dur60-60-120-1.log"
    parser = RawParser()
    df = parser.parse(path)
    print(df)


from parse.runtime_parser import *
def test_runtime_parser():
    path = "/home/yunchi/data/xinda/default/cassandra/rq1_1/writeonly/runtime-cas1-fs-1000000-dur60-60-120-1.log"
    path = "/home/yunchi/data/xinda/default/crdb/rq1_1/a/runtime-roach1-fs-10000-dur60-60-120-1.log"
    path = "/home/yunchi/data/xinda/default/etcd/rq1_1/mixed/runtime-etcd1-nw-high-dur60-60-120-1.log"
    path = "/home/yunchi/data/xinda/default/hbase/rq1_1/readonly/runtime-hbase-regionserver-nw-low-dur40-60-100-1.log"
    parser = RuntimeParser()
    df = parser.parse(path)
    print(df)


from parse.trial_setup_context import *
def test_context_parser():
    path = "/home/yunchi/data/xinda/default/hbase/rq_1/readonly/ts-hbase-regionserver-nw-flaky-medium-dur40-60-100-1.log"
    t = get_trial_setup_context_from_path(path)
    print(t)


test_context_parser()