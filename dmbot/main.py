#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Trevor Day"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import json
from logger import setup_logger
import dmbot

logger = setup_logger(logfile="log.txt")


def main(args):
    """ Main entry point of the app """
    logger.info("hello world")
    logger.info(args)
    with open("secrets.json") as fn:
        secrets = json.load(fn)
        token = secrets["token"]
    dm = dmbot.DMBot(logger)
    dm.run(token)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)
