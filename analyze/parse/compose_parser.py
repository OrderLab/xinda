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
    "hbase": ["slow", "Slow sync", "log roll"],
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


DATA = {
    "#log": 0,
    "#kwlog": 0,
    "#info": 0,
    "#warn": 0,
    "#error": 0,
    "path": []
}

def _compose_basic(log_raw, kws, levels, path):
    data = copy.deepcopy(DATA)
    lines = log_raw.split("\n")
    data["#log"] = len(lines)
    data["path"] = path
    for i, l in enumerate(lines):
        # print(i, len(lines))
        is_slow_log = False
        for kw in kws:
            if kw in l:
                is_slow_log = True
                break
        if is_slow_log:
            data["#kwlog"] += 1
            if levels[0] in l:
                data["#info"] += 1
            elif levels[1] in l:
                data["#warn"] += 1
            else:
                for lvl in levels[2:]:
                    if lvl in l:
                        data["#error"] += 1
                        break
    return data


