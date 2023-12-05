from parse.context import TrialSetupContext

class GenMetaContext:
    def __init__(self, ctx: TrialSetupContext) -> None:
        self.ctx = ctx
        
        self.runtime_csv: str = ""
        self.raw_mrbench_csv: str = ""
        self.raw_teragen_csv: str = ""
        self.raw_terasort_csv: str = ""
        self.info_json: str = ""
        self.compose_json: str = ""
        
        self.producer_csv: str = ""
        self.consumer_csv: str = ""
        self.driver_csv: str = ""
    
        
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
