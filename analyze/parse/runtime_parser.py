import re
import pandas as pd
from collections import defaultdict

from parse.context import get_trial_setup_context_from_path
from parse.tools import read_raw_logfile


COLNAME_TIME = "time(sec)"
COLNAME_TP = "throughput(ops/sec)"
COLNAME_ERR = "errors"
COLNAME_TS = "ts"


class RuntimeParser:
    def __init__(self) -> None:
        self.name = "RuntimeParser"

    def parse(self, path):
        DB_PARSER = {
            ("cassandra", "ycsb"): _runtime_parser_cassandra_ycsb,
            ("crdb",  "ycsb"): _runtime_parser_crdb_ycsb,
            ("crdb",  "sysbench"): _runtime_parser_crdb_sysbench,
            ("etcd", "ycsb"): _runtime_parser_etcd_ycsb,
            ("etcd", "official"): _runtime_parser_etcd_official,
            ("hbase", "ycsb"): _runtime_parser_hbase_ycsb,
        }
        
        t = get_trial_setup_context_from_path(path)
        if t.system in ["hadoop", "kafka"]:
            return None
        
        wl = ""
        if t.workload.startswith("ycsb"):
            wl = "ycsb"
        elif t.workload.startswith("sysbench"):
            wl = "sysbench"
        elif t.workload.startswith("official"):
            wl = "official"
        else: raise NotImplementedError(t.workload)
        result = DB_PARSER[(t.system, wl)](read_raw_logfile(path))
        return result if isinstance(result, tuple) else (result, {})
            


def _runtime_parser_cassandra_ycsb(log_raw):
    pattern = r"(\S* \S*) (\d*) sec:.*; (\S*) current ops\/sec; est completion"
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
    lats = defaultdict(dict)
    lats["unit"] = "ms"
    for line in lines:
        row = line.split()
        try:
            assert row[-1].isalpha()
            if len(row) == 9:
                # time series
                sec = int(float(row[0][:-1]))
                if sec not in data_raw:
                    data_raw[sec] = [0, 0]
                er = float(row[1])
                tp = float(row[2])
                data_raw[sec][0] += tp
                data_raw[sec][1] += er
            elif len(row) == 10:
                pavg, _, p95, p99, _, action = row[4:]
                lats[action].update({
                    "Average": pavg,
                    "p95": p95,
                    "p99": p99
                })
            assert False
        except:
            pass
    data = [[x]+y for x, y in sorted(data_raw.items())]
    df = pd.DataFrame(data, columns=[COLNAME_TIME, COLNAME_TP, COLNAME_ERR])
    return (df, dict(lats))

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
    data = data[:-1]
    
    lats = defaultdict(dict)
    lats["unit"] = "us"
    summary = re.findall(r"(Run finished[\s\S]*)", log_raw)[0]
    lines = re.findall(r"([\S]*)\s*-.*Avg\(us\): (\d*).* 90th\(us\): (\d*).* 95th\(us\): (\d*).* 99th\(us\): (\d*).* 99.9th\(us\): (\d*).* 99.99th\(us\): (\d*)", summary)
    for action, pavg, p90, p95, p99, p999, p9999 in lines:
        lats[action] = {
            "Average": pavg,
            "p90": p90,
            "p95": p95,
            "p99": p99,
            "p999": p999,
            "p9999": p9999
        }
    df = pd.DataFrame(data, columns=[COLNAME_TIME, COLNAME_TP])
    return (df, lats)

def _runtime_parser_etcd_official(log_raw):
    pattern = r"(\d+),.*,.*,.*,(\d+)"
    matches = re.findall(pattern, log_raw)
    data = []
    if matches:
        t0 = int(matches[0][0])
        for t, tp in matches:
            data.append((int(t)-t0, tp))
    df = pd.DataFrame(data, columns=[COLNAME_TIME, COLNAME_TP])
    return df


def _runtime_parser_hbase_ycsb(log_raw):
    return _runtime_parser_cassandra_ycsb(log_raw)
