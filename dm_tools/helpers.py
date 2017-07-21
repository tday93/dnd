import random
import json


class TurnQ(object):

    def __init__(self, start_list=[]):
        self.queue = start_list
        self.sort_self()
        self.pos = 0

    def add(self, name, init):
        self.queue.append((name, init))
        self.sort_self()

    def sort_self(self):
        self.queue = sorted(self.queue, reverse=True, key=lambda f: f[1])

    def next(self):
        response = self.queue[self.pos]
        if self.pos == (len(self.queue) - 1):
            self.pos = 0
        else:
            self.pos += 1
        return response

    def remove(self, name):
        for item in self.queue:
            if item[0] == name:
                self.queue.remove(item)


def roll_dice(roll_string):
    d_split = roll_string.split("d")
    d_amount = int(d_split[0])
    if "+" in d_split[1]:
        d_t_split = d_split[1].split("+")
        d_type = int(d_t_split[0])
        d_add = int(d_t_split[1])
    else:
        d_type = int(d_split[1])
    rolls = []
    for i in range(0, d_amount):
        rolls.append(random.randint(1, d_type))
    if d_add:
        rolls.append(d_add)

    return rolls


class AdvJournal(object):

    def __init__(self, filepath):
        self.journal = read_json(filepath)
        self.filepath = filepath

    def save(self):
        write_json(self.journal, self.filepath)

    def write(self, section_name, text):
        self.journal[section_name].append(text)
        self.save()

    def add_section(self, section_name):
        self.journal[section_name] = []
        self.save()

    def read(self, section_name, num_lines):
        return self.journal[section_name][-num_lines:]

    def make_note(self, text):
        self.journal["notes"].append(text)
        self.save()


def read_json(filepath):
    with open(filepath) as fn:
        return json.load(fn)


def write_json(obj, filepath):
    with open(filepath, "w") as fo:
        json.dump(obj, fo, separators=(", ", ": "), indent=2)
