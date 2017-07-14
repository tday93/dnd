import json
import sys
from random import choice
"""

    madlibbing engine

"""


class Grammar(object):

    def __init__(self, rules):
        self.rules = rules

    def flatten(self, rule_name):
        genned_text = []
        for k, v in self.rules[rule_name].items():
            if k == "pattern":
                for item in v:
                    if item.startswith("#"):
                        genned_text.append(self.flatten(item[1:]))
                    else:
                        genned_text.append(item)
            if k == "bucket":
                selection = choice(v)
                if selection.startswith("#"):
                    genned_text.append(self.flatten(selection[1:]))
                else:
                    genned_text.append(selection)
        return " ".join(genned_text)


def main(filename):
    with open(filename) as fn:
        rules = json.load(fn)
    g = Grammar(rules)
    return(g.flatten("main"))


if __name__ == "__main__":
    filename = sys.argv[1]
    print(main(filename))
