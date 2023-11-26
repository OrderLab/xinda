import json

def read_json(file) -> dict:
    with open(file, "r") as fp:
        return json.load(fp)