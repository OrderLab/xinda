import re
import pandas as pd
from parse.trial_setup_context import get_trial_setup_context_from_path
from parse.tools import read_raw_logfile


COLNAME_TIME = "time(sec)"
COLNAME_TP = "throughput(ops/sec)"
COLNAME_ERR = "errors"


class RuntimeParser:
    def __init__(self) -> None:
        self.name = "RuntimeParser"
        
    def parse(self, path):
        t = get_trial_setup_context_from_path(path)
        DB_PARSER = {
            "cassandra": _runtime_parser_cassandra,
            "crdb": _runtime_parser_crdb,
            "etcd": _runtime_parser_etcd,
            "hadoop": _runtime_parser_hadoop,
            "hbase": _runtime_parser_hbase,
            "kafka": _runtime_parser_kafka,
        }
        parser = DB_PARSER[t.system]
        return parser(read_raw_logfile(path))
    

def _runtime_parser_cassandra(log_raw):
    pattern = r"(\d*) sec:.*; (.*) current ops\/sec;.*, average latency\(us\): \d*\.\d*"
    matches = re.findall(pattern, log_raw)
    data_raw = {}
    for sec, tp in matches:
        data_raw[int(sec)] = data_raw.get(sec, float(tp))
    data = sorted(data_raw.items())
    df = pd.DataFrame(data, columns=[COLNAME_TIME, COLNAME_TP])
    return df


def _runtime_parser_crdb(log_raw):
    lines = log_raw.split("\n")
    data_raw = {}
    for line in lines:
        row = line.split()
        try:
            assert len(row) == 9 and row[-1].isalpha()
            sec = int(float(row[0][:-1]))
            if sec not in data_raw:
                data_raw[sec] = [0,0]
            er = float(row[1])
            tp = float(row[2])
            data_raw[sec][0] += tp
            data_raw[sec][1] += er
        except:
            pass
    data = [[x]+y for x, y in sorted(data_raw.items())]
    df = pd.DataFrame(data, columns=[COLNAME_TIME, COLNAME_TP, COLNAME_ERR])
    return df


def _runtime_parser_etcd(log_raw):
    pattern = r"TOTAL  - Takes\(s\): ([^\s]*), Count: ([^\s]*),"
    matches = re.findall(pattern, log_raw)
    data = []
    for i, _ in enumerate(matches):
        sec, count = _
        last = 0 if i == 0 else float(matches[i-1][1])
        data.append((int(float(sec)), float(count)-last))
    df = pd.DataFrame(data, columns=[COLNAME_TIME, COLNAME_TP])
    return df


def _runtime_parser_hadoop(log_raw):
    return None


def _runtime_parser_hbase(log_raw):
    return _runtime_parser_cassandra(log_raw)

def _runtime_parser_kafka(log_raw):
    return None


if __name__ == "__main__":
    path = "/home/yunchi/data/xinda/default/cassandra/rq1_1/writeonly/runtime-cas1-fs-1000000-dur60-60-120-1.log"
    path = "/home/yunchi/data/xinda/default/crdb/rq1_1/a/runtime-roach1-fs-10000-dur60-60-120-1.log"
    path = "/home/yunchi/data/xinda/default/etcd/rq1_1/mixed/runtime-etcd1-nw-high-dur60-60-120-1.log"
    path = "/home/yunchi/data/xinda/default/hbase/rq1_1/readonly/runtime-hbase-regionserver-nw-low-dur40-60-100-1.log"
    parser = RuntimeParser()
    df = parser.parse(path)
    print(df)
