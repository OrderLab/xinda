import os
import pandas as pd
from typing import Tuple

from parse.context import TrialSetupContext

class GenMetaContext:
    def __init__(self, ctx: TrialSetupContext) -> None:
        self.ctx = ctx
        
        self.runtime_csv: str = ""
        self.raw_mrbench_csv: str = ""
        self.raw_teragen_csv: str = ""
        self.raw_terasort_csv: str = ""
    
    def evaluate(self) -> Tuple[str, str]:
        if self.ctx.system == "hadoop":
            if self.ctx.workload == "mrbench":
                metric = "total_execution_time(ms)"
                df = pd.read_csv(self.raw_mrbench_csv)
                value = df.iloc[-1]["end"] - df.iloc[0]["start"]
            elif self.ctx.workload == "terasort":
                metric = "total_execution_time(ms)"
                start = pd.read_csv(self.raw_teragen_csv).iloc[0]["start"]
                end = pd.read_csv(self.raw_terasort_csv).iloc[-1]["end"]
                value = end - start
            else: raise
        else:
            metric = "average_throughput(ops/sec)"
            value = pd.read_csv(self.runtime_csv)["throughput(ops/sec)"].iloc[30:].mean()
        return metric, str(value)