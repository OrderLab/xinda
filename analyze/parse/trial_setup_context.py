from tools import get_fname, get_dir


class TrialSetupContext:
    def __init__(self) -> None:
        self.action = ""
        self.system = ""
        self.question = ""
        self.workload = ""

        self.log_type = ""
        self.injection_location = ""
        self.injection_type = ""
        self.severity = ""

        self.duration = -1
        self.start = -1
        self.end = -1

        self.iter = -1
    
    def __str__(self) -> str:
        return f"{self.action}, {self.system}, {self.question}, {self.workload}, {self.log_type}, {self.injection_location}, {self.injection_type}, {self.severity}, {self.duration}, {self.start}, {self.end}, {self.iter}"
        
def get_trial_setup_context_from_path(path) -> TrialSetupContext:
    t = TrialSetupContext()

    dir_folders = get_dir(path).split("/")
    assert len(dir_folders) >= 4, dir_folders
    t.action = dir_folders[-4]
    t.system = dir_folders[-3]
    t.question = dir_folders[-2]
    t.workload = dir_folders[-1]

    # handle severity: {slow, flaky}-{low, medium,high}
    # handle container: hbase-*
    tokens = get_fname(path).split("-")
    for s in ["slow", "flaky", "hbase"]:
        if s in tokens:
            i = tokens.index(s)
            tokens[i] += "-" + tokens[i+1]
            tokens = tokens[:i+1] + tokens[i+2:]
    assert len(tokens) in [6,8], tokens
    t.log_type = tokens[0]
    t.injection_location = tokens[1]
    t.injection_type = tokens[2]
    t.severity = tokens[3]
    if len(tokens) == 8:
        t.duration = int(tokens[4][3:])
        t.start = int(tokens[5])
        t.end = int(tokens[6])
    t.iter = int(tokens[-1])

    return t


if __name__ == "__main__":
    path = "/home/yunchi/data/xinda/hbase/rq_1/readonly/ts-hbase-regionserver-nw-flaky-medium-dur40-60-100-1.log"
    t = get_trial_setup_context_from_path(path)
    print(t)


