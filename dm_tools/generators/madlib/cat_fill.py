import json


def ask(prompt):
    return input(prompt)


def fill(filepath):
    pass




def write_json(obj, filepath):
    with open(filepath, "w") as fo:
        json.dump(obj, fo, separators=(", ", ": "), indent=2)


def read_json(filepath):
    with open(filepath) as fn:
        return json.load(fn)
