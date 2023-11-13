import os
import subprocess
import datetime
import time
import yaml
import docker
import psutil
import threading
from xinda.configs.logging import Logging
from xinda.configs.slow_fault import SlowFault
from xinda.configs.tool import Tool
from xinda.configs.benchmark import *

class TestSystem:
    def __init__(self, 
                 sys_name_: str, 
                 fault_: SlowFault, 
                 benchmark_: Benchmark,
                 data_dir_: str,
                 log_root_dir_, #='/users/YXXinda/workdir/data/default',
                 xinda_software_dir_, #= "/users/YXXinda/workdir/xinda-software",
                 xinda_tools_dir_, # = "/users/YXXinda/workdir/xinda/tools",
                 charybdefs_mount_dir_,
                 iter_: int = 1):# = "/users/YXXinda/workdir/tmp"):
        self.sys_name = sys_name_
        self.fault = fault_
        self.log = Logging(sys_name_, data_dir_, fault_, benchmark_, iter_, log_root_dir_)
        self.tool = Tool(sys_name_, xinda_software_dir_, xinda_tools_dir_, charybdefs_mount_dir_)
        self.benchmark = benchmark_
        self.start_time = None
        ct_yaml = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'container.yaml')
        with open(ct_yaml, "r") as config_file:
            self.container_config = yaml.safe_load(config_file)
        if fault_.location not in self.container_config[sys_name_]:
            if sys_name_ != 'etcd':
                raise ValueError(f"Exception: {fault_.location} is not a member of {sys_name_}:{self.container_config[sys_name_]}")
        self.info(f"Current workload: {self.benchmark.workload}")
        self.cleanup()
    
    def cleanup(self):
        client = docker.from_env()
        containers = client.containers.list(all=True)
        # blockade
        for container in containers:
            if container.name == 'dummy':
                self.info('Prior blockade instance detected. Destroying now.')
                cmd = 'blockade destroy'
                _ = subprocess.run(cmd, shell=True, cwd=self.tool.blockade)
                break
        # docker
        if len(containers) > 0:
            self.info(f"Prior docker instance(s) detected. Stopping & removing now.")
            _ = subprocess.run('docker stop $(docker ps -a -q)', shell=True, check=True)
            _ = subprocess.run('docker rm $(docker ps -a -q)', shell=True, check=True)
        # charybdefs
        keyword = "charybdefs"
        process_list = psutil.process_iter(attrs=['pid', 'name', 'cmdline'])
        matching_processes = [process.info for process in process_list if keyword in process.info['name']]
        if len(matching_processes) != 0:
            self.info(f'Prior charybdefs instance detected. Stopping now.')
            charybdefs_dir = matching_processes[0]['cmdline'][2]
            cmd = f'./stop.sh {charybdefs_dir}'
            _ = subprocess.run(cmd, shell=True, cwd=self.tool.cfs_source)
            cmd = f'rm -rf {self.tool.charybdefs_mount_dir}'
            _ = subprocess.run(cmd, shell=True)
            time.sleep(5)
    
    def info(self,
             msg_ : str,
             rela = None,
             if_time = True):
        time_info = ""
        cur_ts = int(time.time()*1e9)
        if rela is None:
            time_info = f"[{str(cur_ts)}, {datetime.datetime.now().strftime('%H:%M:%S')}] "
        else:
            time_info = f"[{str(cur_ts)}, {datetime.datetime.now().strftime('%H:%M:%S')}, {round((cur_ts-rela)/1e9, 3)}] "
        if if_time:
            print('\033[91m' + time_info + msg_ + '\033[0m')
            msg_ = time_info + msg_
        else:
            print('\033[91m' + msg_ + '\033[0m')
        with open(self.log.info, 'a') as fp:
            fp.write("%s\n" % msg_)
    
    def docker_up(self):
        cmd = []
        if self.fault.type == 'nw' or self.fault.type == 'none':
            cmd = ['docker-compose',
                   'up',
                   '-d']
        elif self.fault.type == 'fs':
            cmd = ['docker-compose',
                   '-f', f'docker-compose-{self.fault.location}.yaml',
                   'up',
                   '-d']
        else:
            raise ValueError(f"Exception: Slow fault type:{self.fault.type} is not a member of {{nw, fs, none}}")
        # UP
        _ = subprocess.Popen(cmd, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, cwd=self.tool.compose)
        if self.fault.type == 'fs':
            time.sleep(1)
            print('try again')
            _ = subprocess.Popen(cmd, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, cwd=self.tool.compose)
        self.info('Bringing up a new docker-compose cluster')
        '''
        Why do we have to start the cluster TWICE? I have looked into this problem for a long time. If you:
        1. open a new terminal
        2. cd to charybdefs folder and start charybdefs
        3. cd to docker-xxxx folder
        4. docker-compose up -d to start the service
        5. We will have something similar to 
            "Error response from daemon: error while creating mount source path '/data/ruiming/tmp/cfs_mount/cassandra/cas1': chown /data/ruiming/tmp/cfs_mount/cassandra/cas1: operation not permitted"
        However:
        1. if you docker-compose up -d again, everything works well.
        2. or, if you docker-compose up -d in another terminal when doing step 3/4, everything works well too.
        '''
    
    def charybdefs_up(self):
        def remove_dir(path):
            cmd = f'rm -rf {path}'
            _ = subprocess.run(cmd, shell=True)
        def create_dir(path):
            cmd = f'mkdir {path}'
            _ = subprocess.run(cmd, shell=True)
        if os.path.exists(self.tool.cfs_root):
            remove_dir(self.tool.cfs_root)
            create_dir(self.tool.cfs_root)
        else:
            create_dir(self.tool.cfs_root)
        # clean up the fuser directory
        create_dir(self.tool.cfs_dir)
        create_dir(self.tool.dummy_dir)
        create_dir(self.tool.fuse_dir)
        # start cfs service
        cmd = f"./start.sh {self.tool.fuse_dir} {self.tool.dummy_dir}"
        print(cmd)
        _ = subprocess.run(cmd, shell=True, cwd=self.tool.cfs_source)
        self.info('charybdefs started')
        '''
        # docker-compose up
        # mount_pattern = f"{data_dir}:/var/lib/cassandra/data"
        # cmd = f"CURRENT_UID=$(id -u):$(id -g) DATA_DIR={mount_pattern} docker-compose -f docker-compose-{self.fault.location}.yaml up -d"
        # print(cmd)
        # print(f"_ = subprocess.Popen('{cmd}', shell=True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, cwd={self.tool.compose})")
        # _ = subprocess.Popen(f"'{cmd}'", shell=True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, cwd=self.tool.compose)
        # _ = subprocess.Popen(cmd, shell=True, cwd=self.tool.compose)
        # time.sleep(200)
        # ## docker-compose down
        # cmd = f"CURRENT_UID=$(id -u):$(id -g)  DATA_DIR={data_dir} docker-compose -f docker-compose-{self.fault.location}.yaml down -v"
        # print(cmd)
        # _ = subprocess.Popen(cmd, shell=True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, cwd=self.tool.compose)
        '''
    
    def charybdefs_down(self):
        def remove_dir(path):
            cmd = f'rm -rf {path}'
            _ = subprocess.run(cmd, shell=True)
        # clear errors
        cmd = ['./inject_client',
                   '--clear']
        _ = subprocess.run(cmd, cwd=self.tool.cfs_source)
        # charybdefs down
        cmd = f"./stop.sh {self.tool.fuse_dir}"
        # print(cmd)
        _ = subprocess.run(cmd, shell=True, cwd=self.tool.cfs_source)
        self.info('charybdefs destroyed')
        remove_dir(self.tool.cfs_root)
    
    def docker_status_checker(self):
        pass
    
    def docker_get_status(self):
        containers = self.container_config[self.sys_name]
        client = docker.from_env()
        container_info = {}
        for container_name in containers:
            try:
                container = client.containers.get(container_name)
                container_network = list(container.attrs['NetworkSettings']['Networks'])[0]
                container_info[container.name] = container.attrs['NetworkSettings']['Networks'][container_network]['IPAddress']
            except docker.errors.NotFound:
                print("Container " + container_name + " not found")
        self.container_info = container_info
        self.info('Containers IP addr retrieved')
        for container_name, ip_address in container_info.items():
            self.info(f"Container Name: {container_name}, IP Address: {ip_address}", if_time=False)
        
    
    def docker_down(self) -> subprocess.CompletedProcess:
        cmd = ['docker-compose',
               'down',
               '-v']
        p = subprocess.run(cmd, cwd=self.tool.compose)
        self.info('Docker-compose destroyed')
    
    def blockade_up(self):
        # Create blockade
        cmd = f'blockade --config blockade-{self.fault.severity}.yaml up'
        p = subprocess.run(cmd, cwd=self.tool.blockade, stderr=subprocess.PIPE, shell=True)
        # check return code
        if p.returncode != 0:
            err_msg = p.stderr.decode('utf-8')
            raise Exception(f"Unknown error during blockade initialization. Abort. stderr: {err_msg}.")        
        self.info('Blockade created')
        
        # Add running containers to blockade
        for container_name in list(self.container_info.keys()):
            cmd = ['blockade',
                'add',
                container_name]
            _ = subprocess.run(cmd, cwd=self.tool.blockade)
        self.info('Blockade up and containers added')
        # Check blockade status 
        cmd = ['blockade', 'status']
        p = subprocess.run(cmd, cwd=self.tool.blockade, stdout=subprocess.PIPE)
        self.info(p.stdout.decode('utf-8'), if_time=False)
        # except:
        #     err_msg = p_up.stderr.decode('utf-8')
        #     if 'already exists' in err_msg:
        #         print("Error: a blockade already exists. Trying self.blockade_down() now.")
        #         self.blockade_down()
        #         print("Trying self.blockade_up() again.")
        #         self.blockade_up()
        #     else:
        #         raise subprocess.CalledProcessError("Unknown error during blockade initialization. Abort.")
        
    
    def blockade_down(self):
        cmd = ['blockade',
               '--config',
               ('blockade-' + self.fault.severity + '.yaml'),
               'destroy']
        p = subprocess.run(cmd, cwd=self.tool.blockade)
        self.info('Blockade destroyed')
     
    def test(self):
        pass
    
    def get_current_ts(self, ref=None):
        if ref is None:
            ref = self.start_time
        elapsed_time_in_seconds = (int(time.time()*1e9) - ref)/1e9
        return round(elapsed_time_in_seconds, 3)
    
    def inject(self, cfs_pattern = None):
        if self.start_time is None:
            raise ValueError(f"Exception: self.start_time is None. Either the benchmark has not started yet, or we fail/forget to set this parameter")
        if self.fault.duration == -1:
            self.info("Fault duration == -1, no faults shall be injected")
            return None
        cmd_inject=[]
        cmd_clear=[]
        work_dir=''
        if self.fault.type == 'nw':
            cmd_inject = ['blockade', 'slow', self.fault.location]
            cmd_clear = ['blockade', 'fast', self.fault.location]
            work_dir = self.tool.blockade
        else:
            if cfs_pattern is None:
                cmd_inject = ['./inject_client', '--delay', self.fault.severity]
            else:
                cmd_inject = ['./inject_client', '--pattern', cfs_pattern, '--delay', self.fault.severity]
            cmd_clear = ['./inject_client', '--clear']
            work_dir = self.tool.cfs_source
        # Sleep until fault begins
        cur_time = self.get_current_ts()
        delta_time = self.fault.start_time - cur_time
        self.info(f"Sleep {delta_time} until next command", rela=self.start_time)
        if delta_time > 0:
            time.sleep(delta_time)
        # Faults begin (inject)
        self.info("fault command BEGINs", rela=self.start_time)
        p = subprocess.run(cmd_inject, cwd=work_dir)
        self.info("fault actually BEGINs", rela=self.start_time)
        # Using blockade to inject faults takes nonnegligible time
        # e.g., blockade slow <container_name> could potentially take ~2s
        # So, a fault can last:
        #     Option 1: from <fault.start_time> to <fault.start_time + fault.duration>
        # Or, Option 2: from <fault.start_time> to <fault_actually_begins + fault.duration>
        
        ## Option 1
        # cur_time = self.get_current_ts()
        # delta_time = self.fault.end_time - cur_time
        # if delta_time > 0:
        #     time.sleep(delta_time)
        
        ## Option 2:
        time.sleep(self.fault.duration)
        
        # Faults end (clear)
        self.info("fault command ENDs", rela=self.start_time)
        p = subprocess.run(cmd_clear, cwd=work_dir)
        self.info("fault actually ENDs", rela=self.start_time)