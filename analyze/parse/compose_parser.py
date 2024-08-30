import re
import pandas as pd
import copy

from parse.context import get_trial_setup_context_from_path
from parse.tools import read_raw_logfile


COLNAME_TIME = "time(sec)"
COLNAME_TP = "throughput(ops/sec)"
COLNAME_ERR = "errors"

KWS = {
    "cassandra": ["hinted handoff", "DOWN"],
    "etcd": ["slow", "became leader at term", "heartbeat", "overloaded network", "apply request took too long", "i/o timeout", "peer became inactive", "failed to reach the peer URL", "traceutil/trace.go:171", "overloaded network", "lost TCP streaming connection with remote peer"],
    "hbase": ["slow", "Slow sync", "log roll", "Slow datanode", "an edit"],
    "kafka": ["Error", "timeout "],
    "hadoop": ["Failed to place enough replicas", "Slow", "WARN"],
    "crdb": ["slow" ,"alerts" ,"retry" ,"error" ,"transport" ,"another CREATE STATISTICS job is already running" ,"DistSender.S" , "latch"]
}

class ComposeParser:
    def __init__(self) -> None:
        self.name = "ComposeParser"

    def parse(self, path):
        levels = {
            "cassandra": ["INFO", "WARN", "ERROR"],
            "etcd": ['"level":"info"', '"level":"warn"', '"level":"error"'],
            "hbase": ["INFO", "WARN", "ERROR"],
            "kafka": ["INFO", "WARN", "ERROR"],
            "hadoop": ["INFO", "WARN", "ERROR"],
            "crdb": ["I23", "W23", "E23", "F23"],
        }
        s = get_trial_setup_context_from_path(path).system
        # print(path)
        return _compose_basic(read_raw_logfile(path), kws=KWS[s], levels=levels[s], path=path)


KWSTATS = {
    "#log": 0,
    "#kwlog": 0,
    "#info": 0,
    "#warn": 0,
    "#error": 0,
    "path": "",
    "timestamps": []
}

def _compose_basic(log_raw, kws, levels, path):
    kwstats = copy.deepcopy(KWSTATS)
    lines = log_raw.split("\n")
    kwstats["#log"] = len(lines)
    kwstats["path"] = path
    for i, l in enumerate(lines):
        # print(i, len(lines))
        is_slow_log = False
        
        # check whether contains kw
        for kw in kws:
            if kw in l:
                is_slow_log = True
                break
        
        # count logs by taxonomy
        if is_slow_log:
            kwstats["#kwlog"] += 1
            if levels[0] in l:
                kwstats["#info"] += 1
            elif levels[1] in l:
                kwstats["#warn"] += 1
            else:
                for lvl in levels[2:]:
                    if lvl in l:
                        kwstats["#error"] += 1
                        break
        
            # record timestamps
            matches = re.findall(r"(\d\d:\d\d:\d\d)", l)
            if matches:
                kwstats["timestamps"].append(matches[0])
    return kwstats


