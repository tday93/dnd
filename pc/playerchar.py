import json
from math import floor


class PlayerCharacter(object):

    def __init__(self, filepath):
        self.fp = filepath
        self.data = self.read_json(filepath)
        self.attach_data(self.data)

    def ability_mod(self, a_score):
        return floor(a_score / 2 - 5)

    # data loading and saving
    def attach_data(self, data):
        for k, v in data.items():
            setattr(self, k, v)

    def save_data(self):
        for k, v in self.__dict__.items():
            if k not in ["fp", "data"]:
                self.data[k] = v
        self.write_json(self.data, self.fp)

    def read_json(self, filepath):
        with open(filepath) as fn:
            return json.load(fn)

    def write_json(self, dict_out, filepath):
        with open(filepath, "w") as fo:
            json.dump(dict_out, fo, indent=2, seperators=(',', ':'),
                      sort_keys=True)
