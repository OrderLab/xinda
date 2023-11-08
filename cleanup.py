import docker
import subprocess
import psutil # pip3 install psutil
import time
import datetime
import os
import argparse

def info(msg_ : str,
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

parser = argparse.ArgumentParser(description="Clean up docker containers, blockade, and charybdefs")
parser.add_argument('--docker_aggressive', action='store_true',
                    help='Brute force docker down')
args = parser.parse_args()

# Cleaning up docker-compose containers & blockade
if args.docker_aggressive:
    cmd = "docker ps -a --format \"{{.ID}}\" | xargs docker stop "
    _ = subprocess.run(cmd, shell=True)
    info(f'Stopped all containers')
    cmd = "docker ps -a --format \"{{.ID}}\" | xargs docker rm "
    _ = subprocess.run(cmd, shell=True)
    info(f'Removed all containers')
else:
    client = docker.from_env()
    containers = client.containers.list()
    container_info = {}
    for container in containers:
        container_info[container.name] = container.id
    for name in container_info.keys():
        if name == 'dummy':
            cmd = 'blockade destroy'
            _ = subprocess.run(cmd, shell=True, cwd=f"{os.path.expanduser('~')}/workdir/xinda/tools/blockade")
            info('Blockade destroyed')
            next
        try:
            ct = client.containers.get(container_info[name])
            compose_file_dir = ct.attrs['Config']['Labels']['com.docker.compose.project.working_dir']
            cmd = f'docker-compose down -v'
            _ = subprocess.run(cmd, shell=True, cwd=compose_file_dir)
            info(f'docker-compose down at {compose_file_dir}')
        except:
            pass

# Cleaning up charybdefs
keyword = "charybdefs"
process_list = psutil.process_iter(attrs=['pid', 'name', 'cmdline'])
matching_processes = [process.info for process in process_list if keyword in process.info['name']]
if len(matching_processes) != 0:
    charybdefs_dir = matching_processes[0]['cmdline'][2]
    cmd = f'./stop.sh {charybdefs_dir}'
    _ = subprocess.run(cmd, shell=True, cwd=f"{os.path.expanduser('~')}/workdir/xinda-software/charybdefs")
    info(f'charybdefs stopped at {charybdefs_dir}')
else:
    info('No running charybdefs instance. Skip')