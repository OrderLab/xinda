import re
import json
from typing import Dict
from collections import defaultdict

from parse.tools import read_raw_logfile
from parse.context import get_trial_setup_context_from_path, TrialSetupContext


class InfoParser:
    def __init__(self) -> None:
        self.name = "InfoParser"

    def parse(self, path):
        ctx = get_trial_setup_context_from_path(path)
        data = None
        try:
            data = _info_parser(read_raw_logfile(path), ctx)
        except:
            pass
        return data


def _info_parser(log_raw, ctx: TrialSetupContext) -> Dict:
    pattern_ctx = r"(\{[\s\S]*?\})"
    info_ctx = json.loads("".join(list(re.findall(pattern_ctx, log_raw)[0])))

    pattern_dcup = r", (\S*)\] Containers IP addr retrieved"
    dcup = re.findall(pattern_dcup, log_raw)
    dcup = dcup[0] if len(dcup) > 0 else None

    pattern_tbstart = r", (\S*),.* Sleep \S* until next command"
    tbstart = re.findall(pattern_tbstart, log_raw)
    tbstart = tbstart[0] if len(tbstart) > 0 else None

    pattern_fcmdbegin = r", (\S*), (\S*)\] fault command BEGINs"
    fcmdbegin = re.findall(pattern_fcmdbegin, log_raw)
    fcmdbegin = fcmdbegin[0] if len(fcmdbegin) > 0 else None

    pattern_factualbegin = r", (\S*), (\S*)\] fault actually BEGINs"
    factualbegin = re.findall(pattern_factualbegin, log_raw)
    factualbegin = factualbegin[0] if len(factualbegin) > 0 else None

    pattern_fcmdend = r", (\S*), (\S*)\] fault command ENDs"
    fcmdend = re.findall(pattern_fcmdend, log_raw)
    fcmdend = fcmdend[0] if len(fcmdend) > 0 else None

    pattern_factualend = r", (\S*), (\S*)\] fault actually ENDs"
    factualend = re.findall(pattern_factualend, log_raw)
    factualend = factualend[0] if len(factualend) > 0 else None

    pattern_dcdown = r", (\S*)\] Docker-compose destroyed"
    dcdown = re.findall(pattern_dcdown, log_raw)
    dcdown = dcdown[0] if len(dcdown) > 0 else None
    
    info = {
        "ctx": info_ctx,
        "runtime": {
            "system_up": dcup,
            "testbench_start": tbstart,
            "fault_cmd_begin": fcmdbegin,
            "fault_actual_begin": factualbegin,
            "fault_cmd_end": fcmdend,
            "fault_actual_end": factualend,
            "system_down": dcdown,
        }
    }
    
    if ctx.system == "hadoop" and ctx.workload == "mrbench":
        tasks_unixtime = defaultdict(dict)
        tasks_alignedtime = defaultdict(dict)
        patern_task = r"\[(\d*), .*, (\S+?)\] (\d*) (\S*) \/"
        tasklines = re.findall(patern_task, log_raw)
        for unixtime, alignedtime, task_id, action in tasklines:
            tasks_unixtime[task_id][action] = unixtime
            tasks_alignedtime[task_id][action] = float(alignedtime)
        info["tasks"] = {
            "unix_time": tasks_unixtime,
            "aligned_time": tasks_alignedtime,
        }
    
    if ctx.system == "etcd":
        pattern = r"Leader changed: (\S*)"
        matches = re.findall(pattern, log_raw)
        change = "N/A" if not matches else matches[0][0]
        info["leader_change"] = change
    
    if ctx.system == "hadoop" and ctx.workload == "terasort":
        pattern_start = r", (\S*), (\S*)\] terasort BEGINs"
        terastart = re.findall(pattern_start, log_raw)
        terastart = terastart[0] if len(terastart) > 0 else None
        pattern_end = r", (\S*), (\S*)\] terasort ENDs"
        teraend = re.findall(pattern_end, log_raw)
        teraend = teraend[0] if len(teraend) > 0 else None
        info["tera"] = {
            "begin": terastart,
            "end": teraend
        }
    return info
