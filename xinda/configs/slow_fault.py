import json

class SlowFault:
    def __init__(self, 
                 type_ : str, # nw or fs
                 location_ : str, # e.g., datanode
                 duration_ : int,
                 severity_ : str, # "slow3" for nw; "10000" for fs
                 start_time_ : int,
                 action_ = None):
        self.type = type_
        self.location = location_
        self.duration = duration_
        self.severity = severity_
        self.start_time = start_time_
        self.end_time = start_time_ + duration_
        if type_ == 'none':
            self.info = type_
        elif duration_ == -1:
            self.info = type_ + '-' + severity_ + '-' + 'none'
        else:
            self.info = type_ + '-' + severity_ + '-' + 'dur' + str(duration_) + '-' + str(start_time_) + '-' + str(self.end_time)
    def get_info(self):
        spec = json.dumps(self.__dict__, indent=4)
        print(spec)
        return(spec)