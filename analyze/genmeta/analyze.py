import pandas as pd
from typing import Tuple
from datetime import datetime, timedelta

from genmeta.context import GenMetaContext
from genmeta.tools import read_json
from genmeta.fields import *
from parse.tools import read_raw_logfile

TIME_SEC = "time(sec)"

SHOULD_FILL = "SHOULD_FILL_ERROR"

def gen_stats(gmctx: GenMetaContext):
    # global values
    DUR_MAP = {
        "rq1_1":150,
        "rq1_2":150,
        "rq1_4":1500,
        "restart":300,
        "coverage":150,
        "test":150,
    }
    total_start = 30
    total_end = DUR_MAP[gmctx.ctx.question]
    slow_start, slow_end, fault_actual_begin, fault_actual_end = get_slow_period(gmctx)
    
    # stats
    stats = {}
    
    # parse stats
    if gmctx.ctx.system == "hadoop":
        stats[FIELD_METRIC] = "total_execution_time(s)"
        stats[FIELD_VALUE] = SHOULD_FILL
        stats[FIELD_VAL_IN_SLOW] = SHOULD_FILL
        stats[FIELD_CNT_SLOW_JOBS] = SHOULD_FILL
        
        if gmctx.ctx.workload == "mrbench":
            if not gmctx.info_json: raise MissingParsedLogError("info")
            data = read_json(gmctx.info_json)
            
            try:
                time_tasks = data["tasks"]["aligned_time"]
                task_ids = [int(key) for key in time_tasks]
                min_task_id = min(task_ids)
                max_task_id = max(task_ids)
                stats[FIELD_VALUE] = time_tasks[str(max_task_id)]["ends"] - time_tasks[str(min_task_id+1)]["begins"]
                # slow value
                if slow_start < slow_end: 
                    slow_jobs = []
                    for task_id in time_tasks:
                        s = time_tasks[task_id]["begins"]
                        e = time_tasks[task_id]["ends"]
                        if time_overlap(slow_start, slow_end, s, e):
                            slow_jobs.append((s,e))
                    cnt_slow_jobs = len(slow_jobs)
                    if cnt_slow_jobs:
                        stats[FIELD_VAL_IN_SLOW] = sum([e-s for s,e in slow_jobs]) / cnt_slow_jobs
                    stats[FIELD_CNT_SLOW_JOBS] = cnt_slow_jobs
                else:
                    stats[FIELD_VAL_IN_SLOW] = ""
                    stats[FIELD_CNT_SLOW_JOBS] = ""
            except:
                raise EmptyParsedDataError(gmctx.info_json)
        elif gmctx.ctx.workload == "terasort":
            if not gmctx.raw_teragen_csv: raise MissingParsedLogError("teragen")
            if not gmctx.raw_terasort_csv: raise MissingParsedLogError("terasort")
            df_teragen = pd.read_csv(gmctx.raw_teragen_csv)
            if len(df_teragen) == 0: raise EmptyParsedDataError(gmctx.raw_teragen_csv)
            df_terasort = pd.read_csv(gmctx.raw_terasort_csv)
            if len(df_terasort) == 0: raise EmptyParsedDataError(gmctx.raw_terasort_csv)
            
            if not gmctx.info_json: raise MissingParsedLogError("info")
            data = read_json(gmctx.info_json)
            
            try:
                stats[FIELD_VALUE] = float(data["tera"]["end"][1]) - float(data["tera"]["begin"][1])
            except:
                stats[FIELD_VALUE] = (time_obj(df_terasort.iloc[-1]["end"])-time_obj(df_teragen.iloc[-1]["end"])).total_seconds()
            # slow value
            if slow_start < slow_end: 
                fault_actual_begin_tobj = time_obj(fault_actual_begin) 
                fault_actual_end_tobj = time_obj(fault_actual_end)
                td_begin = 6 if  fault_actual_begin_tobj.hour < 18 else -18
                td_end = 6 if  fault_actual_end_tobj.hour < 18 else -18
                fault_actual_begin_tobj += timedelta(hours=td_begin)
                fault_actual_end_tobj += timedelta(hours=td_end)
                slow_jobs = []
                for _, row in df_terasort.iterrows():
                    _, _, s, e, dur = row
                    if time_overlap(fault_actual_begin_tobj, fault_actual_end_tobj, time_obj(s), time_obj(e)):
                        slow_jobs.append(dur)
                cnt_slow_jobs = len(slow_jobs)
                if cnt_slow_jobs:
                    stats[FIELD_VAL_IN_SLOW] = sum(slow_jobs) / cnt_slow_jobs
                stats[FIELD_CNT_SLOW_JOBS] = cnt_slow_jobs
            else:
                stats[FIELD_VAL_IN_SLOW] = ""
                stats[FIELD_CNT_SLOW_JOBS] = ""
        else: raise
        
    elif gmctx.ctx.system == "kafka":
        stats[FIELD_METRIC] = "average MB.sec"
        stats[FIELD_VALUE] = SHOULD_FILL
        stats[FIELD_VAL_BF_SLOW] = SHOULD_FILL
        stats[FIELD_VAL_IN_SLOW] = SHOULD_FILL
        stats[FIELD_VAL_AF_SLOW] = SHOULD_FILL
        stats[FIELD_RECOVER_TIME] = SHOULD_FILL
        
        if gmctx.ctx.workload == "perf_test":
            if not gmctx.producer_csv: raise MissingParsedLogError("producer")
            if not gmctx.consumer_csv: raise MissingParsedLogError("consumer")
            df_prod = pd.read_csv(gmctx.producer_csv)
            df_cons = pd.read_csv(gmctx.consumer_csv)
            if len(df_prod) == 0: raise EmptyParsedDataError(gmctx.producer_csv)
            if len(df_cons) == 0: raise EmptyParsedDataError(gmctx.consumer_csv)
            
            df_prod = df_prod[(df_prod[TIME_SEC]>=total_start)&(df_prod[TIME_SEC]<=total_end)]
            df_cons = df_cons[(df_cons[TIME_SEC]>=total_start)&(df_cons[TIME_SEC]<=total_end)]
            
            TP = "tp(MB.sec)"
            stats[FIELD_VALUE] = (df_prod[TP].sum()+df_cons[TP].sum()) / (len(df_prod)+len(df_cons))
            if slow_start < slow_end:
                bf_slow_prod = df_prod[df_prod[TIME_SEC]<slow_start]
                bf_slow_cons = df_cons[df_cons[TIME_SEC]<slow_start]
                slow_prod = df_prod[(df_prod[TIME_SEC]>slow_start)&(df_prod[TIME_SEC]<slow_end)]
                slow_cons = df_cons[(df_cons[TIME_SEC]>slow_start)&(df_cons[TIME_SEC]<slow_end)]
                af_slow_prod = df_prod[df_prod[TIME_SEC]>slow_end]
                af_slow_cons = df_cons[df_cons[TIME_SEC]>slow_end]
                if len(bf_slow_prod)*len(slow_prod)*len(af_slow_prod) == 0: 
                    raise EmptySlowFaultDataError(gmctx.producer_csv)
                if len(bf_slow_cons)*len(slow_cons)*len(af_slow_cons) == 0: 
                    raise EmptySlowFaultDataError(gmctx.consumer_csv)
                stats[FIELD_VAL_BF_SLOW] = (bf_slow_prod[TP].sum()+bf_slow_cons[TP].sum()) \
                    /(len(bf_slow_prod)+len(bf_slow_prod))
                stats[FIELD_VAL_IN_SLOW] = (slow_prod[TP].sum()+slow_cons[TP].sum()) \
                    /(len(slow_prod)+len(slow_cons))
                stats[FIELD_VAL_AF_SLOW] = (af_slow_prod[TP].sum()+af_slow_cons[TP].sum()) \
                    /(len(af_slow_prod)+len(af_slow_cons))
                stats[FIELD_RECOVER_TIME] = ""
            else:
                stats[FIELD_VAL_BF_SLOW] = ""
                stats[FIELD_VAL_IN_SLOW] = ""
                stats[FIELD_VAL_AF_SLOW] = ""
                stats[FIELD_RECOVER_TIME] = ""
        elif gmctx.ctx.workload.startswith("openmsg"):
            if not gmctx.driver_csv: raise MissingParsedLogError("openmsg")
            df = pd.read_csv(gmctx.driver_csv)
            if len(df) == 0: raise EmptyParsedDataError(gmctx.driver_csv)
            
            t0 = df[TIME_SEC].iloc[0]
            mask_within_total = df.apply(lambda row: total_start <= sec_from_start(row[TIME_SEC], t0) <= total_end, axis=1)
            df = df[mask_within_total]
            
            PUB_TP, CONS_PT = "pub_tp(MB.sec)", "cons_tp(MB.sec)"
            stats[FIELD_VALUE] = df[[PUB_TP, CONS_PT]].mean().sum() 
            if slow_start < slow_end:
                mask_bf_slow = df.apply(lambda row: total_start <= \
                    sec_from_start(row[TIME_SEC], t0) < sec_from_start(fault_actual_begin, t0, -1), axis=1)
                
                mask_slow = df.apply(lambda row: sec_from_start(fault_actual_begin, t0, -1) < \
                    sec_from_start(row[TIME_SEC], t0) < sec_from_start(fault_actual_end, t0, -1), axis=1)
                
                mask_af_slow = df.apply(lambda row: sec_from_start(fault_actual_end, t0, -1) < \
                    sec_from_start(row[TIME_SEC], t0) <= total_end, axis=1)
                df_bf_slow = df[mask_bf_slow]
                df_slow = df[mask_slow]
                df_af_slow = df[mask_af_slow]
                if len(df_bf_slow)*len(df_slow)*len(df_af_slow) == 0: 
                    raise EmptySlowFaultDataError(gmctx.driver_csv)
                stats[FIELD_VAL_BF_SLOW] = df_bf_slow[[PUB_TP, CONS_PT]].mean().sum()
                stats[FIELD_VAL_IN_SLOW] = df_slow[[PUB_TP, CONS_PT]].mean().sum()
                stats[FIELD_VAL_AF_SLOW] = df_af_slow[[PUB_TP, CONS_PT]].mean().sum()
                
                recov_bar = (df_bf_slow[PUB_TP]+df_bf_slow[CONS_PT]).mean() \
                    - (df_bf_slow[PUB_TP]+df_bf_slow[CONS_PT]).std()
                recover = "inf"
                for i, row in df_af_slow.iterrows():
                    v = df_af_slow.at[i, PUB_TP] + df_af_slow.at[i, CONS_PT]
                    if v >= recov_bar:
                        recover = sec_from_start(df_af_slow.at[i, TIME_SEC], fault_actual_end, 1)
                        break
                stats[FIELD_RECOVER_TIME] = recover
            else:
                stats[FIELD_VAL_BF_SLOW] = ""
                stats[FIELD_VAL_IN_SLOW] = ""
                stats[FIELD_VAL_AF_SLOW] = ""
                stats[FIELD_RECOVER_TIME] = ""
                    
    else: # Cassandra, Crdb, Etcd, HBase
        stats[FIELD_METRIC] = "throughput(ops/sec)"
        stats[FIELD_VALUE] = SHOULD_FILL
        stats[FIELD_VAL_BF_SLOW] = SHOULD_FILL
        stats[FIELD_VAL_IN_SLOW] = SHOULD_FILL
        stats[FIELD_VAL_AF_SLOW] = SHOULD_FILL
        stats[FIELD_RECOVER_TIME] = SHOULD_FILL
        
        if not gmctx.runtime_csv: raise MissingParsedLogError("runtime_csv")
        df = pd.read_csv(gmctx.runtime_csv)
        if len(df) == 0: raise EmptyParsedDataError(gmctx.runtime_csv)
        
        df = df[(df[TIME_SEC]>=total_start)&(df[TIME_SEC]<=total_end)]

        TP = "throughput(ops/sec)"
        stats[FIELD_VALUE] = df[TP].mean()
        
        if slow_start < slow_end:
            df_bf_slow = df[df[TIME_SEC]<slow_start]
            df_slow = df[(df[TIME_SEC]>slow_start)&(df[TIME_SEC]<slow_end)]
            df_af_slow = df[df[TIME_SEC]>slow_end]
            if len(df_bf_slow)*len(df_slow)*len(df_af_slow) == 0: 
                    raise EmptySlowFaultDataError(gmctx.runtime_csv)
            stats[FIELD_VAL_BF_SLOW] = df_bf_slow[TP].mean()
            stats[FIELD_VAL_IN_SLOW] = df_slow[TP].mean()
            stats[FIELD_VAL_AF_SLOW] = df_af_slow[TP].mean()
            
            recov_bar = df_bf_slow[TP].mean() - df_bf_slow[TP].std()
            recover = "inf"
            for i, row in df_af_slow.iterrows():
                v = df.at[i, TP]
                if v >= recov_bar:
                    recover = df.at[i, TIME_SEC] - slow_end
                    break
            stats[FIELD_RECOVER_TIME] = recover
        else:
            stats[FIELD_VAL_BF_SLOW] = ""
            stats[FIELD_VAL_IN_SLOW] = ""
            stats[FIELD_VAL_AF_SLOW] = ""
            stats[FIELD_RECOVER_TIME] = ""
        
        
    if gmctx.ctx.system == "etcd":
        stats[FIELD_LEADER_CHANGED] = SHOULD_FILL
        
        if not gmctx.info_json: raise MissingParsedLogError("info")
        info = read_json(gmctx.info_json)
        stats[FIELD_LEADER_CHANGED] = info["leader_change"]
    
        
    # latency
    stats[FIELD_LAT_R_95] = SHOULD_FILL
    stats[FIELD_LAT_R_99] = SHOULD_FILL
    stats[FIELD_LAT_W_95] = SHOULD_FILL
    stats[FIELD_LAT_W_99] = SHOULD_FILL
    stats[FIELD_LAT_UNIT] = SHOULD_FILL
    
    if gmctx.ctx.system == "cassandra":
        if not gmctx.sum_json: raise MissingParsedLogError("sum")
        lats = read_json(gmctx.sum_json)
        stats[FIELD_LAT_R_95] = lats.get("READ", {}).get("p95", "")
        stats[FIELD_LAT_R_99] = lats.get("READ", {}).get("p99", "")
        stats[FIELD_LAT_W_95] = lats.get("UPDATE", {}).get("p95", "")
        stats[FIELD_LAT_W_99] = lats.get("UPDATE", {}).get("p99", "")
        stats[FIELD_LAT_UNIT] = lats["unit"]
    elif gmctx.ctx.system == "crdb":
        if gmctx.ctx.workload.startswith("ycsb"):
            if not gmctx.runtime_json: raise MissingParsedLogError("runtime_json")
            lats = read_json(gmctx.runtime_json)
            stats[FIELD_LAT_R_95] = lats.get("read", {}).get("p95", "")
            stats[FIELD_LAT_R_99] = lats.get("read", {}).get("p99", "")
            stats[FIELD_LAT_W_95] = lats.get("update", {}).get("p95", "")
            stats[FIELD_LAT_W_99] = lats.get("update", {}).get("p99", "")
            stats[FIELD_LAT_UNIT] = lats["unit"]
        elif gmctx.ctx.workload.startswith("sysbench"):
            pass
    elif gmctx.ctx.system == "etcd":
        if gmctx.ctx.workload.startswith("ycsb"):
            if not gmctx.runtime_json: raise MissingParsedLogError("runtime_json")
            lats = read_json(gmctx.runtime_json)
            stats[FIELD_LAT_R_95] = lats.get("READ", {}).get("p95", "")
            stats[FIELD_LAT_R_99] = lats.get("READ", {}).get("p99", "")
            stats[FIELD_LAT_W_95] = lats.get("UPDATE", {}).get("p95", "")
            stats[FIELD_LAT_W_99] = lats.get("UPDATE", {}).get("p99", "")
            stats[FIELD_LAT_UNIT] = lats["unit"]
        elif gmctx.ctx.workload.startswith("official"):
            pass
    elif gmctx.ctx.system == "hbase":
        if not gmctx.sum_json: raise MissingParsedLogError("sum")
        lats = read_json(gmctx.sum_json)
        stats[FIELD_LAT_R_95] = lats.get("READ", {}).get("p95", "")
        stats[FIELD_LAT_R_99] = lats.get("READ", {}).get("p99", "")
        stats[FIELD_LAT_W_95] = lats.get("UPDATE", {}).get("p95", "")
        stats[FIELD_LAT_W_99] = lats.get("UPDATE", {}).get("p99", "")
        stats[FIELD_LAT_UNIT] = lats["unit"]
    elif gmctx.ctx.system == "hadoop":
        pass
    elif gmctx.ctx.system == "kafka":
        if gmctx.ctx.workload.startswith("openmsg"):
            if not gmctx.driver_json: raise MissingParsedLogError("driver_json")
            lats = read_json(gmctx.driver_json)
            stats[FIELD_LAT_R_95] = ""
            stats[FIELD_LAT_R_99] = ""
            stats[FIELD_LAT_W_95] = lats.get("Pub", {}).get("p95", "")
            stats[FIELD_LAT_W_99] = lats.get("Pub", {}).get("p99", "")
            stats[FIELD_LAT_UNIT] = lats["unit"]
        elif gmctx.ctx.workload == "perf_test":
            pass
        
    
    # stats[FIELD_NUM_LOG] = SHOULD_FILL
    # stats[FIELD_NUM_KWLOG] = SHOULD_FILL
    # stats[FIELD_NUM_INFOLOG] = SHOULD_FILL
    # stats[FIELD_NUM_WARNLOG] = SHOULD_FILL
    # stats[FIELD_NUM_ERRORLOG] = SHOULD_FILL
    # stats[FIELD_FIRST_LOG_TIME] = SHOULD_FILL
    # flt = "not found in slow"
    # if not gmctx.compose_json: raise MissingParsedLogError("compose")
    # info = read_json(gmctx.compose_json)
    # stats[FIELD_NUM_LOG] = info["#log"]
    # stats[FIELD_NUM_KWLOG] = info["#kwlog"]
    # stats[FIELD_NUM_INFOLOG] = info["#info"]
    # stats[FIELD_NUM_WARNLOG] = info["#warn"]
    # stats[FIELD_NUM_ERRORLOG] = info["#error"]
    # if slow_start < slow_end:
    #     raw = read_raw_logfile(info["path"])
    #     ts_begin = time_obj("00"+fault_actual_begin[2:])
    #     for td in range(90):
    #         tstr = (ts_begin + timedelta(seconds=td)).strftime("%H:%M:%S")[2:]
    #         if tstr in raw:
    #             flt = td
    #             break
    # stats[FIELD_FIRST_LOG_TIME] = flt
    
    return stats


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

def sec_from_start(t: str, t0: str, t_hdelta: int = 0) -> float:
    t0_obj = time_obj(t0)
    t_obj = shifted_time_obj(t, t_hdelta)
    d = t_obj - t0_obj
    if d.total_seconds() < 0:
        d += timedelta(hours=24)
    return d.total_seconds()

def shifted_time_obj(t: str, hdelta: int):
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