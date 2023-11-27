import pandas as pd
from typing import Tuple
from datetime import datetime, timedelta

from genmeta.context import GenMetaContext
from genmeta.tools import read_json

TS = "time(sec)"

def gen_stats(gmctx: GenMetaContext) -> Tuple[str, str, str, str]:
    DUR_MAP = {
        "rq1_1":150,
        "rq1_2":150,
        "rq1_4":1500,
        "rq1_5":300
    }
    total_start = 30
    total_end = DUR_MAP[gmctx.ctx.question]
    slow_start, slow_end, fault_actual_begin, fault_actual_end = get_slow_period(gmctx)
    
    metric, value, val_bf_slow, val_slow, val_af_slow, cnt_slow_jobs, leader_change, recover = "", "", "", "", "", "", "", ""
    if gmctx.ctx.system == "hadoop":
        if gmctx.ctx.workload == "mrbench":
            if not gmctx.info_json: raise MissingParsedLogError("info")
            data = read_json(gmctx.info_json)
            
            metric = "total_execution_time(s)"
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
            if slow_start < slow_end: 
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
            df_prod = pd.read_csv(gmctx.producer_csv)
            df_cons = pd.read_csv(gmctx.consumer_csv)
            if len(df_prod) == 0: raise EmptyParsedDataError(gmctx.producer_csv)
            if len(df_cons) == 0: raise EmptyParsedDataError(gmctx.consumer_csv)
            
            df_prod = df_prod[(df_prod[TS]>=total_start)&(df_prod[TS]<=total_end)]
            df_cons = df_cons[(df_cons[TS]>=total_start)&(df_cons[TS]<=total_end)]
            
            metric = "average MB.sec"
            TP = "tp(MB.sec)"
            value = (df_prod[TP].sum()+df_cons[TP].sum()) / (len(df_prod)+len(df_cons))
            if slow_start < slow_end:
                bf_slow_prod = df_prod[df_prod[TS]<slow_start]
                bf_slow_cons = df_cons[df_cons[TS]<slow_start]
                slow_prod = df_prod[(df_prod[TS]>slow_start)&(df_prod[TS]<slow_end)]
                slow_cons = df_cons[(df_cons[TS]>slow_start)&(df_cons[TS]<slow_end)]
                af_slow_prod = df_prod[df_prod[TS]>slow_end]
                af_slow_cons = df_cons[df_cons[TS]>slow_end]
                if len(bf_slow_prod)*len(slow_prod)*len(af_slow_prod) == 0: 
                    raise EmptySlowFaultDataError(gmctx.producer_csv)
                if len(bf_slow_cons)*len(slow_cons)*len(af_slow_cons) == 0: 
                    raise EmptySlowFaultDataError(gmctx.consumer_csv)
                val_bf_slow = (bf_slow_prod[TP].sum()+bf_slow_cons[TP].sum()) \
                    /(len(bf_slow_prod)+len(bf_slow_prod))
                val_slow = (slow_prod[TP].sum()+slow_cons[TP].sum()) \
                    /(len(slow_prod)+len(slow_cons))
                val_af_slow = (af_slow_prod[TP].sum()+af_slow_cons[TP].sum()) \
                    /(len(af_slow_prod)+len(af_slow_cons))
        else:
            if not gmctx.driver_csv: raise MissingParsedLogError("driver")
            df = pd.read_csv(gmctx.driver_csv)
            if len(df) == 0: raise EmptyParsedDataError(gmctx.driver_csv)
            
            t0 = df[TS].iloc[0]
            mask_within_total = df.apply(lambda row: total_start <= sec_from_start(row[TS], t0) <= total_end, axis=1)
            df = df[mask_within_total]
            
            metric = "average MB.sec"
            PUB_TP, CONS_PT = "pub_tp(MB.sec)", "cons_tp(MB.sec)"
            value = df[[PUB_TP, CONS_PT]].mean().sum() 
            if slow_start < slow_end:
                mask_bf_slow = df.apply(lambda row: total_start <= \
                    sec_from_start(row[TS], t0) < sec_from_start(fault_actual_begin, t0), axis=1)
                mask_slow = df.apply(lambda row: sec_from_start(fault_actual_begin, t0) < \
                    sec_from_start(row[TS], t0) < sec_from_start(fault_actual_end, t0), axis=1)
                mask_af_slow = df.apply(lambda row: sec_from_start(fault_actual_end, t0) < \
                    sec_from_start(row[TS], t0) < total_end, axis=1)
                df_bf_slow = df[mask_bf_slow]
                df_slow = df[mask_slow]
                df_af_slow = df[mask_af_slow]
                if len(df_bf_slow)*len(df_slow)*len(df_af_slow) == 0: 
                    raise EmptySlowFaultDataError(gmctx.driver_csv)
                val_bf_slow = df_bf_slow[[PUB_TP, CONS_PT]].mean().sum()
                val_slow = df_slow[[PUB_TP, CONS_PT]].mean().sum()
                val_af_slow = df_af_slow[[PUB_TP, CONS_PT]].mean().sum()
                
                recov_bar = (df_bf_slow[PUB_TP]+df_bf_slow[CONS_PT]).mean() \
                    - (df_bf_slow[PUB_TP]+df_bf_slow[CONS_PT]).std()
                recover = "inf"
                for i, row in df_af_slow.iterrows():
                    v = df_af_slow.at[i, PUB_TP] + df_af_slow.at[i, CONS_PT]
                    if v >= recov_bar:
                        recover = sec_from_start(df_af_slow.at[i, TS], fault_actual_end)
                        break
                    
    else:
        if not gmctx.runtime_csv: raise MissingParsedLogError("runtime")
        df = pd.read_csv(gmctx.runtime_csv)
        if len(df) == 0: raise EmptyParsedDataError(gmctx.runtime_csv)
        
        df = df[(df[TS]>=total_start)&(df[TS]<=total_end)]
        
        metric = "average_throughput(ops/sec)"
        TP = "throughput(ops/sec)"
        value = df[TP].mean()
        if slow_start < slow_end:
            df_bf_slow = df[df[TS]<slow_start]
            df_slow = df[(df[TS]>slow_start)&(df[TS]<slow_end)]
            df_af_slow = df[df[TS]>slow_end]
            if len(df_bf_slow)*len(df_slow)*len(df_af_slow) == 0: 
                    raise EmptySlowFaultDataError(gmctx.runtime_csv)
            val_bf_slow = df_bf_slow[TP].mean()
            val_slow = df_slow[TP].mean()
            val_af_slow = df_af_slow[TP].mean()
            
            recov_bar = val_bf_slow - df_bf_slow[TP].std()
            recover = "inf"
            for i, row in df_af_slow.iterrows():
                v = df.at[i, TP]
                if v >= recov_bar:
                    recover = df.at[i, TS] - slow_end
                    break
        
        if gmctx.ctx.system == "etcd":
            if not gmctx.info_json: raise MissingParsedLogError("info")
            info = read_json(gmctx.info_json)
            leader_change = info["leader_change"]
            
    return metric, str(value), str(val_bf_slow), str(val_slow), str(val_af_slow), str(cnt_slow_jobs), leader_change, recover



def get_slow_period(gmctx: GenMetaContext) -> Tuple[int, int, str, str]:
    if not gmctx.info_json: raise MissingParsedLogError("info")
    info = read_json(gmctx.info_json)
        
    actbeg_rel, actend_rel, actbeg_abs, actend_abs = 0, 0, "", ""
    ctx_start_time = info["ctx"]["start_time"]
    ctx_end_time = info["ctx"]["end_time"]
    if ctx_start_time < ctx_end_time:
        try:
            actbeg_abs, actbeg_rel = info["runtime"]["fault_actual_begin"]
            actend_abs, actend_rel = info["runtime"]["fault_actual_end"]
        except:
            raise UnexpectedInfoFaultNullError(gmctx.info_json)
    return float(actbeg_rel), float(actend_rel), actbeg_abs, actend_abs


def time_overlap(t1_start, t1_end, t2_start, t2_end) -> bool:
    return (t1_start <= t2_end) and (t1_end >= t2_start)

def time_obj(t: str):
    time_format = "%H:%M:%S"
    return datetime.strptime(t, time_format)

def sec_from_start(t: str, t0: str) -> float:
    t0_obj = time_obj(t0)
    t_obj = time_obj(t)
    d = t_obj - t0_obj
    if d.total_seconds() < 0:
        d += timedelta(hours=24)
    return d.total_seconds()

def shifted_time_obj(t: str, hdelta):
    tobj = time_obj(t)
    if tobj.hour + hdelta >= 24:
        hdelta -= 24
    if tobj.hour + hdelta < 0:
        hdelta += 24
    return tobj + timedelta(hours=hdelta)


class MissingParsedLogError(Exception):
    def __init__(self, message):
        super().__init__(message)

class UnexpectedInfoFaultNullError(Exception):
    def __init__(self, message):
        super().__init__(message)
        
class EmptyParsedDataError(Exception):
    def __init__(self, message):
        super().__init__(message)

class EmptySlowFaultDataError(Exception):
    def __init__(self, message):
        super().__init__(message)