import os
class Tool:
    def __init__(self, 
                 sys_name_ : str,
                 root_tool_ = "/data/ruiming/xinda/xinda-software",
                 root_script_ = "/data/ruiming/xinda/tools"):
        
        # Scripts
        self.compose = os.path.join(root_script_, ("docker-" + sys_name_))
        self.blockade = os.path.join(root_script_, "blockade")
        # Tools/Softwares
        self.ycsb = os.path.join(root_tool_, "ycsb-0.17.0")
        self.go_ycsb = os.path.join(root_tool_,"go-ycsb-source")
        self.go_ycsb_bin = os.path.join(root_tool_,"go-ycsb")
        self.cfs_source = os.path.join(root_tool_, "charybdefs")
        self.ycsb_wkl_root =  os.path.join(root_tool_, "ycsb-workloads")
        self.ycsb_wkl = os.path.join(self.ycsb_wkl_root, "ycsb")
        self.go_ycsb_wkl = os.path.join(self.ycsb_wkl_root, "go-ycsb")

        # charybdefs
        self.cfs_root = '/data/ruiming/tmp1'
        # self.cfs_root = '/home/ruiming/temp2'
        self.cfs_dir = os.path.join(self.cfs_root, 'cfs_mount')
        self.fuse_dir = os.path.join(self.cfs_dir, sys_name_)
        self.dummy_dir = os.path.join(self.cfs_root, 'fuser')

        # Cassandra
        self.cas_cqlsh=os.path.join(root_tool_, "cas/bin/cqlsh")
        self.cas_init_cql=os.path.join(root_script_, "init.cql")

        # HBase
        self.hbase_init=os.path.join(root_script_, "hbase-init.sh")
        self.hbase_check_pid=os.path.join(root_script_, "hbase-check-pid.sh")
        self.hbase_ycsb="/tmp/ycsb-0.17.0"
        self.hbase_ycsb_wkl="/tmp/ycsb-workloads/ycsb"

        # MapReduce
        self.mapred_hadoop_local="/data/ruiming/xinda/xinda-software/hadoop-3.2.1/hadoop-mapreduce-project/hadoop-mapreduce-client/hadoop-mapreduce-client-jobclient/target"
        self.mapred_hadoop_container="/opt/hadoop-3.2.1/share/hadoop/mapreduce/"
        self.mapred_mrbench_on_container="/opt/hadoop-3.2.1/share/hadoop/mapreduce/hadoop-mapreduce-client-jobclient-3.2.1-tests.jar"

        # Kafka
        self.kafka = '/data/ruiming/xinda/xinda-software/kafka'