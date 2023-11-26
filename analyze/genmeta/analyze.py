import pandas as pd
from typing import Tuple
from datetime import datetime, timedelta

from genmeta.context import GenMetaContext
from genmeta.tools import read_json

def gen_stats(gmctx: GenMetaContext) -> Tuple[str, str, str, str]:
    metric, value, val_slow, cnt_slow_jobs = "", "", "", ""
    if gmctx.ctx.system == "hadoop":
        if gmctx.ctx.workload == "mrbench":
            if not gmctx.info_json: raise MissingParsedLogError("info")
            data = read_json(gmctx.info_json)
            
            metric = "total_execution_time(s)"
            slow_start, slow_end, _, _ = get_slow_period(gmctx)
            try:
                time_tasks = data["tasks"]["aligned_time"]
                task_ids = [int(key) for key in time_tasks]
                min_task_id = min(task_ids)
                max_task_id = max(task_ids)
                value = time_tasks[str(max_task_id)]["ends"] - time_tasks[str(min_task_id+1)]["begins"]
                # slow value
                slow_jobs = []
                for task_id in time_tasks:
                    s = time_tasks[task_id]["begins"]
                    e = time_tasks[task_id]["ends"]
                    if time_overlap(slow_start, slow_end, s, e):
                        slow_jobs.append((s,e))
                cnt_slow_jobs = len(slow_jobs)
                if cnt_slow_jobs:
                    val_slow = sum([e-s for s,e in slow_jobs]) / cnt_slow_jobs
            except:
                raise EmptyParsedDataError(gmctx.info_json)
        elif gmctx.ctx.workload == "terasort":
            if not gmctx.raw_teragen_csv: raise MissingParsedLogError("teragen")
            if not gmctx.raw_terasort_csv: raise MissingParsedLogError("terasort")
            df_teragen = pd.read_csv(gmctx.raw_teragen_csv)
            if len(df_teragen) == 0: raise EmptyParsedDataError(gmctx.raw_teragen_csv)
            df_terasort = pd.read_csv(gmctx.raw_terasort_csv)
            if len(df_terasort) == 0: raise EmptyParsedDataError(gmctx.raw_terasort_csv)
            
            metric = "total_execution_time(s)"
            value = (time_obj(df_terasort.iloc[-1]["end"])-time_obj(df_teragen.iloc[-1]["end"])).total_seconds()
            # slow value
            _, _, fault_actual_begin, fault_actual_end = get_slow_period(gmctx)
            if fault_actual_begin and fault_actual_end: # deal with non-injection
                fault_actual_begin = time_obj(fault_actual_begin) + timedelta(hours=6)
                fault_actual_end = time_obj(fault_actual_end) + timedelta(hours=6)
                slow_jobs = []
                for _, row in df_terasort.iterrows():
                    _, _, s, e, dur = row
                    if time_overlap(fault_actual_begin, fault_actual_end, time_obj(s), time_obj(e)):
                        slow_jobs.append(dur)
                cnt_slow_jobs = len(slow_jobs)
                if cnt_slow_jobs:
                    val_slow = sum(slow_jobs) / cnt_slow_jobs
        else: raise
    else:
        if not gmctx.runtime_csv: raise MissingParsedLogError("runtime")
        df = pd.read_csv(gmctx.runtime_csv)
        if len(df) == 0: raise EmptyParsedDataError(gmctx.runtime_csv)
        
        metric = "average_throughput(ops/sec)"
        value = df["throughput(ops/sec)"].iloc[30:].mean()
        slow_start, slow_end, _, _ = get_slow_period(gmctx)
        # slow value
        val_slow = df[(df["time(sec)"]>=slow_start)&(df["time(sec)"]<=slow_end)]["throughput(ops/sec)"].mean()
    return metric, str(value), str(val_slow), str(cnt_slow_jobs)


def get_slow_period(gmctx: GenMetaContext) -> Tuple[int, int, str, str]:
    if not gmctx.info_json: raise MissingParsedLogError("info")
    info = read_json(gmctx.info_json)
        
    start, end, fault_actual_begin, fault_actual_end = 0, 0, "", ""
    ctx_start_time = info["ctx"]["start_time"]
    ctx_end_time = info["ctx"]["end_time"]
    if ctx_start_time < ctx_end_time:
        try:
            fault_cmd_begin = info["runtime"]["fault_cmd_begin"]
            fault_actual_begin = info["runtime"]["fault_actual_begin"]
            fault_cmd_end = info["runtime"]["fault_cmd_end"]
            fault_actual_end = info["runtime"]["fault_actual_end"]
            start = ctx_start_time + (time_obj(fault_actual_begin)-time_obj(fault_cmd_begin)).total_seconds()
            end = ctx_end_time + (time_obj(fault_actual_end)-time_obj(fault_cmd_end)).total_seconds()
        except:
            raise UnexpectedInfoFaultNullError(gmctx.info_json)
    return start, end, fault_actual_begin, fault_actual_end

def time_overlap(t1_start, t1_end, t2_start, t2_end) -> bool:
    return (t1_start <= t2_end) and (t1_end >= t2_start)

def time_obj(t):
    time_format = "%H:%M:%S"
    return datetime.strptime(t, time_format)


class MissingParsedLogError(Exception):
    def __init__(self, message):
        super().__init__(message)

class UnexpectedInfoFaultNullError(Exception):
    def __init__(self, message):
        super().__init__(message)
        
class EmptyParsedDataError(Exception):
    def __init__(self, message):
        super().__init__(message)