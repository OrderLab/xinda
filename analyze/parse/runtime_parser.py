import re
import pandas as pd

from parse.context import get_trial_setup_context_from_path
from parse.tools import read_raw_logfile


COLNAME_TIME = "time(sec)"
COLNAME_TP = "throughput(ops/sec)"
COLNAME_ERR = "errors"


class RuntimeParser:
    def __init__(self) -> None:
        self.name = "RuntimeParser"

    def parse(self, path):
        t = get_trial_setup_context_from_path(path)
        if t.system == "hadoop":
            return None
        wl = ""
        if t.workload.startswith("ycsb"):
            wl = "ycsb"
        elif t.workload.startswith("sysbench"):
            wl = "sysbench"
        else: raise
        db_parser_key = (t.system, wl)
        DB_PARSER = {
            ("cassandra", "ycsb"): _runtime_parser_cassandra_ycsb,
            ("crdb",  "ycsb"): _runtime_parser_crdb_ycsb,
            ("crdb",  "sysbench"): _runtime_parser_crdb_sysbench,
            ("etcd", "ycsb"): _runtime_parser_etcd_ycsb,
            ("hbase", "ycsb"): _runtime_parser_hbase_ycsb,
        }
        return DB_PARSER[db_parser_key](read_raw_logfile(path))


def _runtime_parser_cassandra_ycsb(log_raw):
    pattern = r"(\d*) sec:.*; (.*) current ops\/sec;.*, average latency\(us\): \d*\.\d*"
    matches = re.findall(pattern, log_raw)
    data_raw = {}
    for sec, tp in matches:
        data_raw[int(sec)] = data_raw.get(sec, float(tp))
    data = sorted(data_raw.items())
    df = pd.DataFrame(data, columns=[COLNAME_TIME, COLNAME_TP])
    return df


def _runtime_parser_crdb_ycsb(log_raw):
    lines = log_raw.split("\n")
    data_raw = {}
    for line in lines:
        row = line.split()
        try:
            assert len(row) == 9 and row[-1].isalpha()
            sec = int(float(row[0][:-1]))
            if sec not in data_raw:
                data_raw[sec] = [0, 0]
            er = float(row[1])
            tp = float(row[2])
            data_raw[sec][0] += tp
            data_raw[sec][1] += er
        except:
            pass
    data = [[x]+y for x, y in sorted(data_raw.items())]
    df = pd.DataFrame(data, columns=[COLNAME_TIME, COLNAME_TP, COLNAME_ERR])
    return df

def _runtime_parser_crdb_sysbench(log_raw):
    pattern = r"\[ (\d*)s \].* tps: ([\S]*).* err\/s: ([\S]*)"
    matches = re.findall(pattern, log_raw)
    data = matches
    df = pd.DataFrame(data, columns=[COLNAME_TIME, COLNAME_TP, COLNAME_ERR])
    return df

def _runtime_parser_etcd_ycsb(log_raw):
    pattern = r"TOTAL  - Takes\(s\): ([^\s]*), Count: ([^\s]*),"
    matches = re.findall(pattern, log_raw)
    data = []
    for i, _ in enumerate(matches):
        sec, count = _
        last = 0 if i == 0 else float(matches[i-1][1])
        data.append((int(float(sec)), float(count)-last))
    df = pd.DataFrame(data, columns=[COLNAME_TIME, COLNAME_TP])
    return df


def _runtime_parser_hbase_ycsb(log_raw):
    return _runtime_parser_cassandra_ycsb(log_raw)
