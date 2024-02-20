class ResourceLimit:
    def __init__(self, 
                 cpu_limit_ : str, # e.g., datanode
                 mem_limit_ : str):
        if cpu_limit_ is None or mem_limit_ is None:
            raise ValueError(f"At least one of the following is NoneType: CPU_LIMIT={self.reslim.cpu_limit} MEM_LIMIT={self.reslim.mem_limit}")
        self.cpu_limit = cpu_limit_
        self.mem_limit = mem_limit_