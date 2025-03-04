import os


def get_dir(path) -> str:
    return os.path.dirname(path)


def get_fname(path) -> str:
    basename = os.path.basename(path)
    fname, ext = os.path.splitext(basename)
    return fname


def read_raw_logfile(path) -> str:
    with open(path, "r") as fp:
        return fp.read()
    

def ensure_dirs(path) -> None:
    dir_path = os.path.dirname(path)
    os.makedirs(dir_path, exist_ok=True)