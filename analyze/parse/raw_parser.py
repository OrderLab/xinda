import re
import pandas as pd

from parse.context import get_trial_setup_context_from_path
from parse.tools import read_raw_logfile

COLNAME_JOBID = "job_id"
COLNAME_TASKID = "task_id"
COLNAME_START = "start"
COLNAME_END = "end"
COLNAME_DURATION = "duration(ms)"


class RawParser:
    def __init__(self) -> None:
        self.name = "RawParser"

    def parse(self, path):
        t = get_trial_setup_context_from_path(path)
        if t.system not in DB_PARSER:
            return None
        
        DB_PARSER = {
            "hadoop": _raw_parser_hadoop,
            "terasort": _raw_parser_hadoop,
        }
        return DB_PARSER[t.system](read_raw_logfile(path))


def _raw_parser_hadoop(log_raw):
    pattern = r"TaskID:([\w\d]*).*duration: (\d*) - (\d*) = (\d*)"
    matches = re.findall(pattern, log_raw)
    data = []
    for task_id_raw, end, start, dur in matches:
        task_tokens = task_id_raw.split("_")
        job_id = "_".join(["job"]+task_tokens[1:3])
        task_id = "_".join(task_tokens[-2:])
        data.append((job_id, task_id, start, end, dur))
    df = pd.DataFrame(data, columns=[
                      COLNAME_JOBID, COLNAME_TASKID, COLNAME_START, COLNAME_END, COLNAME_DURATION])
    return df
