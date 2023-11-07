import os


def get_dir(path):
    return os.path.dirname(path)


def get_fname(path):
    basename = os.path.basename(path)
    fname, ext = os.path.splitext(basename)
    return fname


def read_raw_logfile(path):
    with open(path, "r") as fp:
        return fp.read()