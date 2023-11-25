import json
import pandas as pd
from typing import Tuple
from datetime import datetime

from parse.context import TrialSetupContext

class GenMetaContext:
    def __init__(self, ctx: TrialSetupContext) -> None:
        self.ctx = ctx
        
        self.runtime_csv: str = ""
        self.raw_mrbench_csv: str = ""
        self.raw_teragen_csv: str = ""
        self.raw_terasort_csv: str = ""
        self.info_json: str = ""
    
    def evaluate(self) -> Tuple[str, str]:
        metric, value, val_slow = "", 0, 0
        if self.ctx.system == "hadoop":
            if self.ctx.workload == "mrbench":
                if not self.raw_mrbench_csv: raise MissingParsedLogError("mrbench")
                df = pd.read_csv(self.raw_mrbench_csv)
                if len(df) == 0: raise EmptyParsedDataError(self.raw_mrbench_csv)
                
                metric = "total_execution_time(ms)"
                value = df.iloc[-1]["end"] - df.iloc[0]["start"]
            elif self.ctx.workload == "terasort":
                if not self.raw_teragen_csv: raise MissingParsedLogError("teragen")
                if not self.raw_terasort_csv: raise MissingParsedLogError("terasort")
                df_teragen = pd.read_csv(self.raw_teragen_csv)
                if len(df_teragen) == 0: raise EmptyParsedDataError(self.raw_teragen_csv)
                df_terasort = pd.read_csv(self.raw_terasort_csv)
                if len(df_terasort) == 0: raise EmptyParsedDataError(self.raw_terasort_csv)
                
                metric = "total_execution_time(ms)"
                value = df_terasort.iloc[-1]["end"] - df_teragen.iloc[0]["start"]
            else: raise
        else:
            if not self.runtime_csv: raise MissingParsedLogError("runtime")
            df = pd.read_csv(self.runtime_csv)
            if len(df) == 0: raise EmptyParsedDataError(self.runtime_csv)
            
            metric = "average_throughput(ops/sec)"
            value = df["throughput(ops/sec)"].iloc[30:].mean()
            slow_start, slow_end = self.slow_period
            val_slow = df[(df["time(sec)"]>=slow_start)&(df["time(sec)"]<=slow_end)]["throughput(ops/sec)"].mean()
        return metric, str(value), str(val_slow)
    
    @property
    def slow_period(self) -> Tuple[int, int]:
        info = {}
        if not self.info_json: raise MissingParsedLogError("info")
        with open(self.info_json, "r") as fp:
            info = json.load(fp)
            
        start, end = 0, 0
        time_format = "%H:%M:%S"
        ctx_start_time = info["ctx"]["start_time"]
        ctx_end_time = info["ctx"]["end_time"]
        if ctx_start_time < ctx_end_time:
            try:
                fault_cmd_begin = datetime.strptime(info["runtime"]["fault_cmd_begin"], time_format)
                fault_actual_begin = datetime.strptime(info["runtime"]["fault_actual_begin"], time_format)
                fault_cmd_end = datetime.strptime(info["runtime"]["fault_cmd_end"], time_format)
                fault_actual_end = datetime.strptime(info["runtime"]["fault_actual_end"], time_format)
                start = ctx_start_time + (fault_actual_begin-fault_cmd_begin).total_seconds()
                end = ctx_end_time + (fault_actual_end-fault_cmd_end).total_seconds()
            except:
                raise UnexpectedInfoFaultNullError(self.info_json)
        return start, end
        
    @property
    def profile(self) -> str:
        s = f"path:{self.ctx.path},\n"
        s += f"ctx:{self.ctx},\n"
        s += f"runtime_csv:{self.runtime_csv},\n"
        s += f"raw_mrbench_csv:{self.raw_mrbench_csv},\n"
        s += f"raw_teragen_csv:{self.raw_teragen_csv},\n"
        s += f"raw_terasort_csv:{self.raw_terasort_csv},\n"
        s += f"info_json:{self.info_json}"
        return s

class MissingParsedLogError(Exception):
    def __init__(self, message):
        super().__init__(message)

class UnexpectedInfoFaultNullError(Exception):
    def __init__(self, message):
        super().__init__(message)
        
class EmptyParsedDataError(Exception):
    def __init__(self, message):
        super().__init__(message)