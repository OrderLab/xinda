import os
from parse.tools import get_fname, get_dir


class TrialSetupContext:
    def __init__(self) -> None:
        self.path = ""
        
        self.action = ""
        self.system = ""
        self.question = ""
        self.workload = ""
        self.cpu = ""
        self.mem = ""

        self.log_type = ""
        self.injection_location = ""
        self.injection_type = ""
        self.severity = ""

        self.duration: int = 0
        self.start: int = 0
        self.end: int = 0

        self.iter: int = 0
        self.suffix: str = ""
        
        self.version = ""
    
    def __str__(self) -> str:
        return f"{self.action}, {self.system}, {self.version}, {self.question}, {self.workload}, {self.cpu}, {self.mem}, {self.log_type}, {self.injection_location}, {self.injection_type}, {self.severity}, {self.duration}, {self.start}, {self.end}, {self.iter}, {self.suffix}"

        
def get_trial_setup_context_from_path(path) -> TrialSetupContext:
    t = TrialSetupContext()
    t.path = path

    dir_folders = get_dir(path).split("/")
    assert len(dir_folders) >= 4, dir_folders
    tokens = get_fname(path).split("-")
    
    # backward compatibility of cpu and mem limit
    if not (dir_folders[-2].startswith("cpu") and  dir_folders[-1].startswith("mem")):
        dir_folders += ["cpu_unbounded", "mem_unbounded"]
    
    if "kafka" in dir_folders:  # handle kafka
        if dir_folders[-6] == "kafka":
            # .../sensitivity_1s_p1/kafka/rq1_1/openmsg-1-topic-1-partition-1kb/kafka-throughput/cpu_3/mem_512M/compose-kafka1-nw-flaky-p1-dur30-60-90-1.log
            t.action = dir_folders[-7]
            t.system = dir_folders[-6]
            t.question = dir_folders[-5]  
            t.workload = dir_folders[-4] + "|" + dir_folders[-3]
            t.cpu = dir_folders[-2]
            t.mem = dir_folders[-1]
        elif dir_folders[-5] == "kafka" and dir_folders[-4] == "perf_test":
            t.action = dir_folders[-6]
            t.system = dir_folders[-5]
            t.question = dir_folders[-4]
            t.workload = dir_folders[-3]
            t.cpu = dir_folders[-2]
            t.mem = dir_folders[-1]
        else:
            assert False, f"ignore {path}"   
    else:   # all other systems
        if os.path.split(path)[1] in ["cockroach.log", "cockroach.json"]:
            tokens = get_fname(dir_folders[-1]).split("-")
            dir_folders = dir_folders[:-1]
        t.action = dir_folders[-6]
        t.system = dir_folders[-5]
        t.question = dir_folders[-4]
        t.workload = dir_folders[-3]
        t.cpu = dir_folders[-2]
        t.mem = dir_folders[-1]
    t.system, t.version = (t.system.split("-") + [""])[:2]

    # handle severity: {slow, flaky}-{low, medium,high}
    # handle container: hbase-*
    if t.system == "hadoop":
        if tokens[-1] in ["terasort", "teragen"] or tokens[-1].startswith("mrbench"):
            t.suffix = tokens[-1]
            tokens = tokens[:-1]
    for s in ["slow", "flaky", "hbase"]:
        if s in tokens:
            i = tokens.index(s)
            tokens[i] += "-" + tokens[i+1]
            tokens = tokens[:i+1] + tokens[i+2:]
    for s in ["restart"]:
        if s in tokens:
            i = tokens.index(s)
            tokens = tokens[:i] + tokens[i+1:]
    assert len(tokens) in [6,8], f"{path} -> {tokens}"
    t.log_type = tokens[0]
    t.injection_location = tokens[1]
    t.injection_type = tokens[2]
    t.severity = tokens[3]
    if len(tokens) == 6:
        t.iter = int(tokens[5])
    if len(tokens) in [8,9]:
        t.duration = int(tokens[4][3:])
        t.start = int(tokens[5])
        t.end = int(tokens[6])
        t.iter = int(tokens[7])
    if t.log_type == "crlog":
        t.log_type = "compose"
    return t
