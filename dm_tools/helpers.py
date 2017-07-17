import random


class TurnQ(object):

    def __init__(self, start_list):
        self.queue = start_list
        self.sort_self()
        self.pos = 0

    def add(self, name, init):
        self.queue.append((name, init))
        self.sort_self()

    def sort_self(self):
        self.queue = sorted(self.queue, reversed=True, key=lambda f: f[1])

    def next(self):
        print(self.queue[self.pos])
        if self.pos == (len(self.queue) - 1):
            self.pos = 0
        else:
            self.pos += 1

    def remove(self, name):
        self.queue.remove(name)


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
