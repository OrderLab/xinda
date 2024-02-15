class ResourceLimit:
    def __init__(self, 
                 if_reslim_ : bool = False, # nw or fs
                 cpu_limit_ : str = None, # e.g., datanode
                 mem_limit_ : str = None):
        self.if_reslim = if_reslim_
        if if_reslim_:
            if cpu_limit_ is None or mem_limit_ is None:
                raise Exception(f'Resource limits enabled (if_reslim={if_reslim_}), but at least one of cpu_limit ({cpu_limit_}) or mem_limit ({mem_limit_}) is None')      
                exit(1)
        self.cpu_limit = cpu_limit_
        self.mem_limit = mem_limit_