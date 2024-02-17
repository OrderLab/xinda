import argparse
import os
import logging
import json
import pandas as pd
from pandas import DataFrame
from tqdm import tqdm
from collections import OrderedDict

from config import DATA_DIR
from typing import List, Tuple, Dict
from parse.runtime_parser import RuntimeParser
from parse.raw_parser import RawParser
from parse.info_parser import InfoParser
from parse.compose_parser import ComposeParser
from parse.sum_parser import SummaryParser
from parse.context import get_trial_setup_context_from_path, TrialSetupContext
from parse.kafka_parser import PerfConsumerParser, PerfProducerParser, OpenMsgDriverParser
from genmeta.context import GenMetaContext
from genmeta.analyze import gen_stats, EmptyParsedDataError, MissingParsedLogError, UnexpectedInfoFaultNullError, EmptySlowFaultDataError
from genmeta.fields import STATS_COLNAMES, FIELD_PARSE_ERROR, FIELD_SRC_INFO, FIELD_SRC_RUNTIME, FIELD_SRC_RAW, FIELD_SRC_KAFKA


PARSERS = {
    "runtime":(RuntimeParser, ["csv", "json"]),
    "raw":(RawParser, ["csv"]),
    "info":(InfoParser, ["json"]),
    "producer":(PerfProducerParser, ["csv"]),
    "consumer":(PerfConsumerParser, ["csv"]),
    "driver":(OpenMsgDriverParser, ["csv"]),
    "sum":(SummaryParser, ["json"]),
    # "compose": (ComposeParser, ["json"])
}


def get_all_files(data_dir, exts=[".log"]) -> List[str]:
    paths = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            paths.append(os.path.join(root, file))
    return [p for p in paths if os.path.splitext(p)[-1] in exts]


def parse_single(log_path, output_path_woext, parser) -> None:
    ctx = get_trial_setup_context_from_path(log_path)
    data = parser.parse(log_path)
    if data is None:
        logging.info(
            f"Unimplemented {ctx.system} {parser.name} for {log_path}. ")
    else:
        if isinstance(data, dict) or isinstance(data, DataFrame):
            data = [data]
        for d in data:
            if isinstance(d, dict):
                p = output_path_woext + ".json"
                with open(p, 'w') as fp:
                    json.dump(d, fp, indent=4)
            else:
                try:
                    p = output_path_woext + ".csv"
                    d.to_csv(p, index=False)
                except:
                    print(d)
                    raise


def parse_batch(data_dir, output_dir, redo_exists) -> None:
    log_ctx = {}
    for p in get_all_files(data_dir):
        try:
            log_ctx[p] = get_trial_setup_context_from_path(p)
        except:
            logging.warn(f"Skip {p}. Cannot parse context from filename.")

    for path, ctx in tqdm(log_ctx.items()):
        psrname = ctx.log_type
        if psrname not in PARSERS:
            continue
        parser, exts = PARSERS[psrname]
        outpath_woext = os.path.splitext(path.replace(data_dir, output_dir))[0]
        if psrname not in redo_exists:
            all_exists = True
            for ext in exts:
                all_exists = all_exists and os.path.exists(outpath_woext + f".{ext}")
            if all_exists:
                continue
        os.makedirs(os.path.dirname(outpath_woext), exist_ok=True)
        parse_single(path, outpath_woext, parser())


def hash_tsctx(ctx: TrialSetupContext) -> Tuple:
    return (ctx.action, ctx.system, ctx.version, ctx.question, ctx.workload, \
        ctx.injection_location, ctx.injection_type, ctx.severity, \
        ctx.start, ctx.duration, ctx.iter)


def gen_meta_batch(data_dir, output_dir) -> None:
    parsed_data_files = get_all_files(data_dir, exts=[".csv", ".json"])
    outpath = os.path.join(output_dir, "meta.csv")
    if outpath in parsed_data_files:
        parsed_data_files.remove(outpath)
    
    genmeta_tasks: Dict[Tuple, GenMetaContext] = {}
    for p in parsed_data_files:
        ctx = get_trial_setup_context_from_path(p)
        key = hash_tsctx(ctx)
        if key not in genmeta_tasks:
            genmeta_tasks[key] = GenMetaContext(ctx)
        # compose
        if ctx.log_type == "compose":
            genmeta_tasks[key].compose_json = p
        # info
        if ctx.log_type == "info":
            genmeta_tasks[key].info_json = p
        # runtime
        if ctx.system != "hadoop" and  ctx.log_type == "runtime":
            if p.endswith(".csv"):
                genmeta_tasks[key].runtime_csv = p
            elif p.endswith(".json"):
                genmeta_tasks[key].runtime_json = p
        # raw 
        if ctx.system == "hadoop" and ctx.log_type == "raw":
            if ctx.workload == "mrbench":
                genmeta_tasks[key].raw_mrbench_csv = p
            elif ctx.workload == "terasort":
                if ctx.suffix == "teragen":
                    genmeta_tasks[key].raw_teragen_csv = p
                elif ctx.suffix == "terasort":
                    genmeta_tasks[key].raw_terasort_csv = p
                else: raise
            else: raise
        # kafka
        if ctx.system == "kafka":
            if ctx.log_type == "producer":
                genmeta_tasks[key].producer_csv = p
            elif ctx.log_type == "consumer":
                genmeta_tasks[key].consumer_csv = p
            elif ctx.log_type == "driver":
                if p.endswith(".csv"):
                    genmeta_tasks[key].driver_csv = p
                elif p.endswith(".json"):
                    genmeta_tasks[key].driver_json = p
        # sum
        if ctx.log_type == "sum":
            genmeta_tasks[key].sum_json = p
            
    meta = []
    colnames = [
        "rq", 
        "system", 
        "workload", 
        "fault_type", 
        "fault_location", 
        "fault_duration", 
        "fault_start", 
        "fault_severity", 
        "iter_flag"] + STATS_COLNAMES
    for key, gmctx in tqdm(genmeta_tasks.items()):
        full_stats = OrderedDict({k:"" for k in STATS_COLNAMES})
        err = ""
        try:
            stats = gen_stats(gmctx)
        except (EmptyParsedDataError, 
                MissingParsedLogError, 
                UnexpectedInfoFaultNullError, 
                EmptySlowFaultDataError) as e:
            err = f"{type(e).__name__}:{e}"
            
        for k in stats.keys():
            assert k in STATS_COLNAMES, k
        full_stats.update(stats)
        
        full_stats[FIELD_PARSE_ERROR] = err
        full_stats[FIELD_SRC_INFO] = gmctx.info_json
        full_stats[FIELD_SRC_RUNTIME] = gmctx.runtime_csv
        full_stats[FIELD_SRC_RAW] = f"{gmctx.raw_mrbench_csv},{gmctx.raw_terasort_csv}"
        full_stats[FIELD_SRC_KAFKA] = f"{gmctx.producer_csv},{gmctx.producer_csv},{gmctx.driver_csv}"
        row = [
            gmctx.ctx.question,
            gmctx.ctx.system + gmctx.ctx.version,
            gmctx.ctx.workload,
            gmctx.ctx.injection_type,
            gmctx.ctx.injection_location,
            gmctx.ctx.duration,
            gmctx.ctx.start,
            gmctx.ctx.severity,
            gmctx.ctx.iter] + list(full_stats.values())
        meta.append(row)

    df = pd.DataFrame(sorted(meta), columns=colnames)
    df.to_csv(outpath, index=False)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="xinda log parser")
    parser.add_argument("-d", "--data_dir", default=DATA_DIR,
                        help="Specify root of data directory containing all logs")
    parser.add_argument("-o", "--output_dir", default=None,
                        help="Specify root of output directory for outputing all logs")
    parser.add_argument("-r", "--redo", default="",
                        help="Redo tasks")

    args = parser.parse_args()
    output_dir = os.path.abspath(args.output_dir or args.data_dir.replace("/data/ruiming", "/data/yunchi"))


    parse_batch(
        data_dir=os.path.abspath(args.data_dir),
        output_dir=output_dir,
        redo_exists=args.redo.split(",")
    )
    
    gen_meta_batch(
        data_dir=output_dir,
        output_dir=output_dir,
    )
