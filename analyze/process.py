import argparse
import os
import logging
import json
import pandas as pd
from tqdm import tqdm

from config import DATA_DIR, OUTPUT_DIR
from typing import List, Tuple, Dict
from parse.runtime_parser import RuntimeParser
from parse.raw_parser import RawParser
from parse.info_parser import InfoParser
from parse.context import get_trial_setup_context_from_path, TrialSetupContext
from parse.kafka_parser import PerfConsumerParser, PerfProducerParser, OpenMsgDriverParser
from genmeta.context import GenMetaContext
from genmeta.analyze import gen_stats, EmptyParsedDataError, MissingParsedLogError, UnexpectedInfoFaultNullError


PARSERS = {
    "runtime": RuntimeParser,
    "raw": RawParser,
    "info": InfoParser,
    "producer": PerfProducerParser,
    "consumer": PerfConsumerParser,
    "driver": OpenMsgDriverParser
}


def get_all_files(data_dir, exts=[".log"]) -> List[str]:
    paths = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            paths.append(os.path.join(root, file))
    return [p for p in paths if os.path.splitext(p)[-1] in exts]


def parse_single(log_path, output_path, parser) -> None:
    ctx = get_trial_setup_context_from_path(log_path)
    data = parser.parse(log_path)
    if data is None:
        logging.info(
            f"Unimplemented {ctx.system} {parser.name} for {log_path}. ")
    elif isinstance(data, dict):
        with open(output_path, 'w') as fp:
            json.dump(data, fp, indent=4)
    else:
        data.to_csv(output_path, index=False)


def parse_batch(data_dir, output_dir, redo_exists) -> None:
    log_ctx = {}
    for p in get_all_files(data_dir):
        try:
            log_ctx[p] = get_trial_setup_context_from_path(p)
        except:
            logging.info(f"Skip {p}. Cannot parse context from filename.")

    for path, ctx in tqdm(log_ctx.items()):
        psrname = ctx.log_type
        if psrname not in PARSERS:
            continue
        ext = ".json" if psrname == "info" else ".csv"
        outpath = os.path.splitext(path.replace(data_dir, output_dir))[0] + ext
        if psrname not in redo_exists and os.path.exists(outpath):
            continue
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        parse_single(path, outpath, PARSERS[psrname]())


def hash_tsctx(ctx: TrialSetupContext) -> Tuple:
    return (ctx.action, ctx.system, ctx.question, ctx.workload, \
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
        # info
        if ctx.log_type == "info":
            genmeta_tasks[key].info_json = p
        # runtime
        if ctx.system != "hadoop" and  ctx.log_type == "runtime":
            genmeta_tasks[key].runtime_csv = p
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
                genmeta_tasks[key].driver_csv = p
    
    meta = []
    meta_colnames = ["rq", "system", "workload", "fault_type", "fault_location", \
        "fault_duration", "fault_start", "fault_severity", "iter_flag", \
        "metric", "value", "val_slow", "cnt_slow_jobs", "ERROR", "INFO", "RUNTIME", "RAW", "KAFKA"]
    for key, gmctx in tqdm(genmeta_tasks.items()):
        metric, value, val_slow, cnt_slow_jobs, err = "N/A", "N/A", "N/A", "", ""
        try:
            metric, value, val_slow, cnt_slow_jobs = gen_stats(gmctx)
        except (EmptyParsedDataError, MissingParsedLogError, UnexpectedInfoFaultNullError) as e:
            err = f"{type(e).__name__}:{e}"
        meta.append((gmctx.ctx.question, gmctx.ctx.system, gmctx.ctx.workload, \
            gmctx.ctx.injection_type, gmctx.ctx.injection_location, \
            gmctx.ctx.duration, gmctx.ctx.start, gmctx.ctx.severity, gmctx.ctx.iter, \
            metric, value, val_slow, cnt_slow_jobs, err, \
            gmctx.info_json, gmctx.runtime_csv, f"{gmctx.raw_mrbench_csv},{gmctx.raw_terasort_csv}",\
            f"{gmctx.producer_csv},{gmctx.producer_csv},{gmctx.driver_csv}"))
    df = pd.DataFrame(sorted(meta), columns=meta_colnames)
    df.to_csv(outpath, index=False)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="xinda log parser")
    parser.add_argument("-d", "--data_dir", default=DATA_DIR,
                        help="Specify root of data directory containing all logs")
    parser.add_argument("-o", "--output_dir", default=OUTPUT_DIR,
                        help="Specify root of output directory for outputing all logs")
    parser.add_argument("-r", "--redo", default="",
                        help="Redo tasks")

    args = parser.parse_args()


    parse_batch(
        data_dir=os.path.abspath(args.data_dir),
        output_dir=os.path.abspath(args.output_dir),
        redo_exists=args.redo.split(",")
    )
    
    gen_meta_batch(
        data_dir=os.path.abspath(args.output_dir),
        output_dir=os.path.abspath(args.output_dir),
    )
