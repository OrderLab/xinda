import argparse
import os
import logging
import json

from config import DATA_DIR, OUTPUT_DIR
from typing import List
from parse.runtime_parser import RuntimeParser
from parse.raw_parser import RawParser
from parse.info_parser import InfoParser
from parse.trial_setup_context import get_trial_setup_context_from_path

PARSERS = {
    "runtime": RuntimeParser,
    "raw": RawParser,
    "info": InfoParser,
}


def get_all_logpaths(data_dir, ext=".log") -> List[str]:
    paths = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            paths.append(os.path.join(root, file))
    return [p for p in paths if os.path.splitext(p)[-1] == ext]


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


def parse_batch(data_dir, output_dir, parser_names) -> None:
    log_ctx = {}
    for l in get_all_logpaths(data_dir):
        try:
            log_ctx[l] = get_trial_setup_context_from_path(l)
        except:
            logging.warning(f"Skip {l}. Cannot parse context from filename.")

    for psrname in parser_names:
        target_paths = [l for l, ctx in log_ctx.items()
                        if ctx.log_type == psrname]
        for path in target_paths:
            ext = ".json" if psrname == "info" else ".csv"
            outpath = os.path.splitext(path.replace(
                data_dir, output_dir))[0] + ext
            if os.path.exists(outpath):
                continue
            os.makedirs(os.path.dirname(outpath), exist_ok=True)
            parse_single(path, outpath, PARSERS[psrname]())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="xinda log parser")
    parser.add_argument("-d", "--data_dir", default=DATA_DIR,
                        help="Specify root of data directory containing all logs")
    parser.add_argument("-o", "--output_dir", default=OUTPUT_DIR,
                        help="Specify root of output directory for outputing all logs")
    parser.add_argument("-p", "--parser", default=None,
                        help="Specify the target parser name. Default for all.")

    args = parser.parse_args()
    parser_names = args.parser.split(
        ",") if args.parser is not None else list(PARSERS.keys())
    for pname in parser_names:
        if pname not in PARSERS:
            raise ValueError(f"{pname} parser is not supported")

    parse_batch(
        data_dir=os.path.abspath(args.data_dir),
        output_dir=os.path.abspath(args.output_dir),
        parser_names=parser_names)
