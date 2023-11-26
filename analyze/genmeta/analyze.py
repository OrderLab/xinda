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
            df_teragen = pd.read_csv(gmctx.raw_teragen_csv).iloc[30:]
            if len(df_teragen) == 0: raise EmptyParsedDataError(gmctx.raw_teragen_csv)
            df_terasort = pd.read_csv(gmctx.raw_terasort_csv).iloc[30:]
            if len(df_terasort) == 0: raise EmptyParsedDataError(gmctx.raw_terasort_csv)
            
            metric = "total_execution_time(s)"
            value = (time_obj(df_terasort.iloc[-1]["end"])-time_obj(df_teragen.iloc[-1]["end"])).total_seconds()
            # slow value
            _, _, fault_actual_begin, fault_actual_end = get_slow_period(gmctx)
            if fault_actual_begin and fault_actual_end: # deal with non-injection
                fault_actual_begin = time_obj(fault_actual_begin) 
                fault_actual_end = time_obj(fault_actual_end)
                td_begin = 6 if  fault_actual_begin.hour < 18 else -18
                td_end = 6 if  fault_actual_end.hour < 18 else -18
                fault_actual_begin += timedelta(hours=td_begin)
                fault_actual_end += timedelta(hours=td_end)
                slow_jobs = []
                for _, row in df_terasort.iterrows():
                    _, _, s, e, dur = row
                    if time_overlap(fault_actual_begin, fault_actual_end, time_obj(s), time_obj(e)):
                        slow_jobs.append(dur)
                cnt_slow_jobs = len(slow_jobs)
                if cnt_slow_jobs:
                    val_slow = sum(slow_jobs) / cnt_slow_jobs
        else: raise
    elif gmctx.ctx.system == "kafka":
        if gmctx.ctx.workload == "perf_test":
            if not gmctx.producer_csv: raise MissingParsedLogError("producer")
            if not gmctx.consumer_csv: raise MissingParsedLogError("consumer")
            df_prod = pd.read_csv(gmctx.producer_csv).iloc[30:]
            if len(df_prod) == 0: raise EmptyParsedDataError(gmctx.producer_csv)
            df_cons = pd.read_csv(gmctx.consumer_csv).iloc[30:]
            if len(df_cons) == 0: raise EmptyParsedDataError(gmctx.consumer_csv)
            
            metric = "average MB.sec"
            value = (df_prod["tp(MB.sec)"].sum()+df_cons["tp(MB.sec)"].sum()) / (len(df_prod)+len(df_cons))
            # slow value
            slow_start, slow_end, _, _ = get_slow_period(gmctx)
            slow_prod = df_prod[(df_prod["time(sec)"]>=slow_start)&(df_prod["time(sec)"]<=slow_end)]
            slow_cons = df_cons[(df_cons["time(sec)"]>=slow_start)&(df_cons["time(sec)"]<=slow_end)]
            if (len(slow_prod)+len(slow_cons)):
                val_slow = (slow_prod["tp(MB.sec)"].sum()+slow_cons["tp(MB.sec)"].sum()) / (len(slow_prod)+len(slow_cons))
        else:
            if not gmctx.driver_csv: raise MissingParsedLogError("driver")
            df = pd.read_csv(gmctx.driver_csv)
            if len(df) == 0: raise EmptyParsedDataError(gmctx.driver_csv)
            
            metric = "average MB.sec"
            value = df[["pub_tp(MB.sec)", "cons_tp(MB.sec)"]].mean().sum() 
            # slow value
            _, _, fault_actual_begin, fault_actual_end = get_slow_period(gmctx)
            if fault_actual_begin and fault_actual_end: # deal with non-injection
                tp = []
                fault_actual_begin = time_obj(fault_actual_begin)
                fault_actual_end = time_obj(fault_actual_end)
                for _, row in df.iterrows():
                    t = time_obj(row["time(sec)"])
                    td = 1 if t.hour < 23 else -23
                    t += timedelta(hours=td)
                    if fault_actual_begin <= t <= fault_actual_end:
                        tp.append((row["pub_tp(MB.sec)"] + row["cons_tp(MB.sec)"]) / 2)
                if tp:
                    val_slow = sum(tp) / len(tp)
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
        
    start, end, fault_actual_begin, fault_actual_end, fault_cmd_end = 0, 0, "", "", ""
    ctx_start_time = info["ctx"]["start_time"]
    ctx_end_time = info["ctx"]["end_time"]
    ctx_duration = info["ctx"]["duration"]
    if ctx_start_time < ctx_end_time:
        try:
            fault_cmd_begin = info["runtime"]["fault_cmd_begin"]
            fault_actual_begin = info["runtime"]["fault_actual_begin"]
            fault_cmd_end = info["runtime"]["fault_cmd_end"]
            fault_actual_end = info["runtime"]["fault_actual_end"]
            start = ctx_start_time + (time_obj(fault_actual_begin)-time_obj(fault_cmd_begin)).total_seconds()
            end = start + ctx_duration + (time_obj(fault_actual_end)-time_obj(fault_cmd_end)).total_seconds()
        except:
            raise UnexpectedInfoFaultNullError(gmctx.info_json)
    # return ctx_start_time, ctx_end_time, fault_actual_begin, fault_actual_end
    # return start, end, fault_actual_begin, fault_actual_end
    return start, ctx_end_time, fault_actual_begin, fault_cmd_end

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