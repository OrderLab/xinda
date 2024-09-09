import os
from xinda.configs.reslim import *

class Tool:
    def __init__(self, 
                 sys_name_ : str,
                 xinda_software_dir_ : str, #= "/data/ruiming/xinda/xinda-software",
                 xinda_tools_dir_ : str, #= "/data/ruiming/xinda/tools",
                 charybdefs_mount_dir_ : str,
                 reslim_: ResourceLimit,
                 version_: str = None,
                 coverage_: bool = False,
                 coverage_dir_: str = None,
                 change_workload_: bool = False,
                 ):
        self.version = version_
        self.xinda_software_dir = xinda_software_dir_
        self.xinda_tools_dir = xinda_tools_dir_
        self.charybdefs_mount_dir = charybdefs_mount_dir_
        self.reslim = reslim_
        # Scripts
        self.jacoco = os.path.join(xinda_tools_dir_, ('docker-' + sys_name_), 'jacoco')
        if version_ != None:
            self.compose = os.path.join(xinda_tools_dir_, ("docker-" + sys_name_), version_)
        else:
            self.compose = os.path.join(xinda_tools_dir_, ("docker-" + sys_name_))

        if coverage_ and sys_name_ == 'etcd':
            self.compose = os.path.join(self.compose, "coverage")
        self.coverage_dir = coverage_dir_

        if coverage_:
            # create coverage folder
            os.makedirs(self.coverage_dir, mode=0o777, exist_ok=True)
        else:
            print("Coverage is not enabled, ignore coverage folder creation")

        print("Using compose files inside: ", self.compose)
        # test if the compose folder exists
        if not os.path.exists(self.compose):
            raise FileNotFoundError(f"Compose folder {self.compose} does not exist, check your version and coverage arguments")

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
        if change_workload_ and sys_name_ == 'hbase':
            self.hbase_init=os.path.join(xinda_tools_dir_, "hbase-init2.sh")
            print('Copying hbase-init2.sh')
        self.hbase_check_pid=os.path.join(xinda_tools_dir_, "hbase-check-pid.sh")
        self.hbase_ycsb="/tmp/ycsb-0.17.0"
        self.hbase_ycsb_wkl="/tmp/ycsb-workloads/ycsb"

        # MapReduce
        self.hadoop_mapreduce_client_local=os.path.join(xinda_software_dir_, f"hadoop-{version_}/hadoop-mapreduce-project/hadoop-mapreduce-client/hadoop-mapreduce-client-jobclient/target")
        self.mapred_hadoop_container=f"/opt/hadoop-{version_}/share/hadoop/mapreduce/"
        self.mapred_mrbench_on_container=f"/opt/hadoop-{version_}/share/hadoop/mapreduce/hadoop-mapreduce-client-jobclient-{version_}-tests.jar"
        
        self.hadoop_mapreduce_examples_local=os.path.join(xinda_software_dir_, f"hadoop-{version_}/hadoop-mapreduce-project/hadoop-mapreduce-examples/target")
        self.mapred_terasort_on_container=f"/opt/hadoop-{version_}/share/hadoop/mapreduce/hadoop-mapreduce-examples-{version_}.jar"

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
            #    'CONTAINER_DIR_etcd=/data.etcd/data1',
               'CONTAINER_DIR_etcd=/data.etcd',
               f'LOCAL_DIR_etcd1={self.fuse_dir}/etcd1',
               f'LOCAL_DIR_etcd2={self.fuse_dir}/etcd2',
               f'COVER_DIR_etcd0={self.coverage_dir}/etcd0',
               f'COVER_DIR_etcd1={self.coverage_dir}/etcd1',
               f'COVER_DIR_etcd2={self.coverage_dir}/etcd2',

               # hadoop
               f'LOCAL_DIR_datanode={self.fuse_dir}/datanode',
               'CONTAINER_DIR_datanode=/hadoop/dfs/data',
               f'LOCAL_DIR_namenode={self.fuse_dir}/namenode',
               'CONTAINER_DIR_namenode=/hadoop/dfs/name',
               f'LOCAL_DIR_historyserver={self.fuse_dir}/historyserver',
               'CONTAINER_DIR_historyserver=/hadoop/yarn/timeline',
               f'LOCAL_DIR_nodemanager={self.fuse_dir}/nodemanager',
               f'CONTAINER_DIR_nodemanager=/opt/hadoop-{self.version}/logs',
               # hbase
               f'LOCAL_DIR_datanode_hbase={self.fuse_dir}/datanode',
               f'LOCAL_DIR_namenode_hbase={self.fuse_dir}/namenode',
               # kafka
               f'LOCAL_DIR_kafka1={self.fuse_dir}/kafka1',
               f'LOCAL_DIR_kafka2={self.fuse_dir}/kafka2',
               f'LOCAL_DIR_kafka3={self.fuse_dir}/kafka3',
               f'LOCAL_DIR_kafka4={self.fuse_dir}/kafka4',
               'CONTAINER_DIR_kafka=/bitnami',
               # resource limits
               f'CPU_LIMIT={self.reslim.cpu_limit}',
               f'MEM_LIMIT={self.reslim.mem_limit}',
               ]
        with open(env_path, "w") as file:
            for line in msg:
                file.write(line + "\n")