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
    try:
        with open(CONFIG_PATH, "r") as config_file:
            config = json.loads(config_file.read())
    except FileNotFoundError:
        with open(CONFIG_PATH, "w") as config_file:
            config_file.write(json.dumps(DEFAULT_CONFIG, indent=4))

            print(f"Missing {CONFIG_PATH}")
            return

    try:
        user = search.search("user_data", "id", str(config["user_id"]))[0]
        print(user)
    except IndexError:
        print("Invalid user id")
        return

    match args[1]:
        case "add":
            add.main(*args[1:])

        case "remove":
            remove.main(*args[1:])

        case "search":
            search.main(*args[1:])

    with open(CONFIG_PATH, "w") as config_file:
        config_file.write(json.dumps(config, indent=4))


if __name__ == "__main__":
    main(*sys.argv)
