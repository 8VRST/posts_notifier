from pathlib import Path
import json


def open_json_file(path_to_file):
    with open(Path(path_to_file), encoding="utf-8") as open_file:
        data = json.load(open_file)
    return data