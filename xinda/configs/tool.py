import os
class Tool:
    def __init__(self, 
                 sys_name_ : str,
                 xinda_software_dir_ : str, #= "/data/ruiming/xinda/xinda-software",
                 xinda_tools_dir_ : str, #= "/data/ruiming/xinda/tools",
                 charybdefs_mount_dir_ : str): #= "/data/ruiming/tmp1"):
        
        # Scripts
        self.compose = os.path.join(xinda_tools_dir_, ("docker-" + sys_name_))
        self.blockade = os.path.join(xinda_tools_dir_, "blockade")
        # Tools/Softwares
        self.ycsb = os.path.join(xinda_software_dir_, "ycsb-0.17.0")
        self.go_ycsb = os.path.join(xinda_software_dir_,"go-ycsb-source")
        self.go_ycsb_bin = os.path.join(xinda_software_dir_,"go-ycsb")
        self.cfs_source = os.path.join(xinda_software_dir_, "charybdefs")
        self.ycsb_wkl_root =  os.path.join(xinda_software_dir_, "ycsb-workloads")
        self.ycsb_wkl = os.path.join(self.ycsb_wkl_root, "ycsb")
        self.go_ycsb_wkl = os.path.join(self.ycsb_wkl_root, "go-ycsb")

        # charybdefs
        self.cfs_root = charybdefs_mount_dir_
        # self.cfs_root = '/home/ruiming/temp2'
        self.cfs_dir = os.path.join(self.cfs_root, 'cfs_mount')
        self.fuse_dir = os.path.join(self.cfs_dir, sys_name_)
        self.dummy_dir = os.path.join(self.cfs_root, 'fuser')

        # Cassandra
        self.cas_cqlsh=os.path.join(xinda_software_dir_, "cas/bin/cqlsh")
        self.cas_init_cql=os.path.join(xinda_tools_dir_, "init.cql")

        # HBase
        self.hbase_init=os.path.join(xinda_tools_dir_, "hbase-init.sh")
        self.hbase_check_pid=os.path.join(xinda_tools_dir_, "hbase-check-pid.sh")
        self.hbase_ycsb="/tmp/ycsb-0.17.0"
        self.hbase_ycsb_wkl="/tmp/ycsb-workloads/ycsb"

        # MapReduce
        self.hadoop_mapreduce_client_local=os.path.join(xinda_software_dir_, "hadoop-3.2.1/hadoop-mapreduce-project/hadoop-mapreduce-client/hadoop-mapreduce-client-jobclient/target")
        self.mapred_hadoop_container="/opt/hadoop-3.2.1/share/hadoop/mapreduce/"
        self.mapred_mrbench_on_container="/opt/hadoop-3.2.1/share/hadoop/mapreduce/hadoop-mapreduce-client-jobclient-3.2.1-tests.jar"
        
        self.hadoop_mapreduce_examples_local=os.path.join(xinda_software_dir_, "hadoop-3.2.1/hadoop-mapreduce-project/hadoop-mapreduce-examples/target")
        self.mapred_terasort_on_container="/opt/hadoop-3.2.1/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.1.jar"

        # Kafka
        self.kafka_compiled_source = os.path.join(xinda_software_dir_, 'kafka')
        self.openmsg_compiled_source = '/data/ruiming/temp/openmessaging' # test use only (on razor14)
        # self.openmsg_compiled_source = os.path.join(xinda_software_dir_, 'openmessaging')
