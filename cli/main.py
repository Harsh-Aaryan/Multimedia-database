#!/usr/bin/env python3


from constants import *
import add
import argparse
import json
import psycopg
import random
import remove
import search
import sys
import time


def main(*args) -> None:
    match args[1]:
        case "add":
            add.main(*args[1:])

        case "remove":
            remove.main(*args[1:])

        case "search":
            search.main(*args[1:])


if __name__ == "__main__":
    main(*sys.argv)
