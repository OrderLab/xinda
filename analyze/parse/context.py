from parse.tools import get_fname, get_dir


class TrialSetupContext:
    def __init__(self) -> None:
        self.path = ""
        
        self.action = ""
        self.system = ""
        self.question = ""
        self.workload = ""

        self.log_type = ""
        self.injection_location = ""
        self.injection_type = ""
        self.severity = ""

        self.duration: int = 0
        self.start: int = 0
        self.end: int = 0

        self.iter: int = 0
        self.suffix: str = ""
    
    def __str__(self) -> str:
        return f"{self.action}, {self.system}, {self.question}, {self.workload}, {self.log_type}, {self.injection_location}, {self.injection_type}, {self.severity}, {self.duration}, {self.start}, {self.end}, {self.iter}, {self.suffix}"

        
def get_trial_setup_context_from_path(path) -> TrialSetupContext:
    t = TrialSetupContext()
    t.path = path

    dir_folders = get_dir(path).split("/")
    assert len(dir_folders) >= 4, dir_folders
    t.action = dir_folders[-4]
    t.system = dir_folders[-3]
    t.question = dir_folders[-2]
    t.workload = dir_folders[-1]

    # handle severity: {slow, flaky}-{low, medium,high}
    # handle container: hbase-*
    tokens = get_fname(path).split("-")
    if t.system == "hadoop":
        if tokens[-1] in ["terasort", "teragen"] or tokens[-1].startswith("mrbench"):
            t.suffix = tokens[-1]
            tokens = tokens[:-1]
    for s in ["slow", "flaky", "hbase"]:
        if s in tokens:
            i = tokens.index(s)
            tokens[i] += "-" + tokens[i+1]
            tokens = tokens[:i+1] + tokens[i+2:]
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
    return t
