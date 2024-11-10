#!/usr/bin/env python3


from constants import *
import argparse
import json
import psycopg
import random
import sys
import time


def main(*args) -> None:
    # with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
    #     with conn.cursor() as cur:
    #         cur.execute("SELECT * FROM user_data;")

    #         for record in cur.fetchone():
    #             print(record)
    new_media(args[1], int(args[2]))


if __name__ == "__main__":
    main(*sys.argv)
