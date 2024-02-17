import re
import pandas as pd

from parse.tools import read_raw_logfile


COLNAME_TIME = "time(sec)"
COLNAME_PERF_TP_MSG = "tp(nMsg.sec)"
COLNAME_PERF_TP_SIZE = "tp(MB.sec)"


class PerfProducerParser:
    def __init__(self) -> None:
        self.name = "PerfProducerParser"

    def parse(self, path):
        log_raw = read_raw_logfile(path)
        pattern = r".*, (\S*) records\/sec \((\S*) MB\/sec\)"
        matches = re.findall(pattern, log_raw)
        data = []
        for i, row in enumerate(matches):
            data.append((i, row[0], row[1]))
        df = pd.DataFrame(data, columns=[COLNAME_TIME, COLNAME_PERF_TP_MSG, COLNAME_PERF_TP_SIZE])
        return df


class PerfConsumerParser:
    def __init__(self) -> None:
        self.name = "PerfConsumerParser"

    def parse(self, path):
        df = pd.read_csv(path)
        df.rename(columns={" nMsg.sec": COLNAME_PERF_TP_MSG}, inplace=True)
        df.rename(columns={" MB.sec": COLNAME_PERF_TP_SIZE}, inplace=True)
        df[COLNAME_TIME] = df.index
        df = df[[COLNAME_TIME, COLNAME_PERF_TP_MSG, COLNAME_PERF_TP_SIZE]]
        return df

COLNAME_OM_PUB_TP_MSG = "pub_tp(nMsg.sec)"
COLNAME_OM_PUB_TP_SIZE = "pub_tp(MB.sec)"
COLNAME_OM_PUB_ERR = "err(err.sec)"

COLNAME_OM_CONS_TP_MSG = "cons_tp(nMsg.sec)"
COLNAME_OM_CONS_TP_SIZE = "cons_tp(MB.sec)"


class OpenMsgDriverParser:
    def __init__(self) -> None:
        self.name = "OpenMsgDriverParser"

    def parse(self, path):
        log_raw = read_raw_logfile(path)
        log_after_warmup = re.findall(r"----- Starting benchmark traffic \(1m\)------([\s\S]*)", log_raw)[0]
        
        pattern = r"(\S*)\..* Pub rate\s*(\S*) msg\/s \/\s*(\S*) MB\/s .* (\S*) err\/s \| Cons rate\s*(\S*) msg\/s \/\s*(\S*) MB\/s"
        matches = re.findall(pattern, log_after_warmup)
        
        df = pd.DataFrame(matches, columns=[COLNAME_TIME, COLNAME_OM_PUB_TP_MSG, COLNAME_OM_PUB_TP_SIZE, COLNAME_OM_PUB_ERR, COLNAME_OM_CONS_TP_MSG, COLNAME_OM_CONS_TP_SIZE])
        return df