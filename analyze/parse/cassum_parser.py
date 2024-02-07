import re
import pandas as pd
from collections import defaultdict

from parse.context import get_trial_setup_context_from_path
from parse.tools import read_raw_logfile


class CassandraSummaryParser:
    def __init__(self) -> None:
        self.name = "CassandraSummaryParser"

    def parse(self, path):
        DB_PARSER = {
            "cassandra": _sum_parser_cassandra,
        }
        
        t = get_trial_setup_context_from_path(path)
        if t.system not in DB_PARSER:
            return None
        return DB_PARSER[t.system](read_raw_logfile(path))


def _sum_parser_cassandra(log_raw):
    actions = ["READ", "UPDATE"]
    pctgs = ["p90", "p95", "p99", "p99.9", "p99.99", "Average"]
    data = defaultdict(dict)
    for a in actions:
        for p in pctgs:
            pattern = r"\[" + a + r"\], " + p + r", (\S*)"
            matches = re.findall(pattern, log_raw)
            data["unit"] = "microsecond"
            data[a][p] = matches[0] if matches else None
    return dict(data)