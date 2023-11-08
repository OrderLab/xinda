import os
class Tool:
    def __init__(self, 
                 sys_name_ : str,
                 xinda_software_dir_ : str, #= "/data/ruiming/xinda/xinda-software",
                 xinda_tools_dir_ : str, #= "/data/ruiming/xinda/tools",
                 charybdefs_mount_dir_ : str): #= "/data/ruiming/tmp1"):
        
        self.xinda_software_dir = xinda_software_dir_
        self.xinda_tools_dir = xinda_tools_dir_
        self.charybdefs_mount_dir = charybdefs_mount_dir_
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
        # self.openmsg_compiled_source = '/data/ruiming/temp/openmessaging' # test use only (on razor14)
        self.openmsg_compiled_source = os.path.join(xinda_software_dir_, 'openmessaging')
        self.generate_env()
    
    def generate_env(self):
        env_path = f'{self.compose}/.env'
        uid = os.getuid()
        gid = os.getgid()
        msg = [f"UID={uid}",
               f"GID={gid}",
               f"GID_KAFKA=0",
               # Cassandra
               f'LOCAL_DIR_cas1={self.fuse_dir}/cas1',
               f'LOCAL_DIR_cas2={self.fuse_dir}/cas2',
               'CONTAINER_DIR_cas=/var/lib/cassandra/data',
               # crdb
               f'LOCAL_DIR_roach1={self.fuse_dir}/roach1',
               'CONTAINER_DIR_roach1=/cockroach/cockroach-data',
               f'LOCAL_DIR_roach2={self.fuse_dir}/roach2',
               'CONTAINER_DIR_roach2=/cockroach/cockroach-data',
               # etcd
               f'LOCAL_DIR_etcd0={self.fuse_dir}/etcd0',
               'CONTAINER_DIR_etcd0=/data.etcd',
               f'LOCAL_DIR_etcd0={self.fuse_dir}/etcd1',
               'CONTAINER_DIR_etcd0=/data.etcd',
               # hadoop
               f'LOCAL_DIR_datanode={self.fuse_dir}/datanode',
               'CONTAINER_DIR_datanode=/hadoop/dfs/data',
               f'LOCAL_DIR_namenode={self.fuse_dir}/namenode',
               'CONTAINER_DIR_namenode=/hadoop/dfs/name',
               f'LOCAL_DIR_historyserver={self.fuse_dir}/historyserver',
               'CONTAINER_DIR_historyserver=/hadoop/yarn/timeline',
               f'LOCAL_DIR_nodemanager={self.fuse_dir}/nodemanager',
               'CONTAINER_DIR_nodemanager=/opt/hadoop-3.2.1/logs',
               # hbase
               f'LOCAL_DIR_datanode_hbase={self.fuse_dir}/datanode',
               f'LOCAL_DIR_namenode_hbase={self.fuse_dir}/namenode',
               f'LOCAL_DIR_kafka1={self.fuse_dir}/kafka1',
               f'LOCAL_DIR_kafka2={self.fuse_dir}/kafka2',
               f'LOCAL_DIR_kafka3={self.fuse_dir}/kafka3',
               f'LOCAL_DIR_kafka4={self.fuse_dir}/kafka4',
               'CONTAINER_DIR_kafka=/bitnami']
        with open(env_path, "w") as file:
            for line in msg:
                file.write(line + "\n")