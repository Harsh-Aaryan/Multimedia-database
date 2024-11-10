#!/usr/bin/env python3


import argparse
import json
import psycopg
import random
import sys
import time


DATABASE_NAME = "multimedia_db"
DATABASE_USER = "postgres"
POSTGRES_MAX_INTEGER_SIZE = 2147483647
POSTGRES_MAX_BIGINT_SIZE = 9223372036854775807


def new_id() -> int:
    return random.randrange(POSTGRES_MAX_INTEGER_SIZE)


def new_media(title: str, release_year: int) -> None:
    media_id = new_id()
    creation_time_posix = int(time.time())

    with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO media VALUES (%s, %s, %s, %s)",
                (media_id, title, creation_time_posix, release_year)
            )


def main(*args) -> None:
    # with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
    #     with conn.cursor() as cur:
    #         cur.execute("SELECT * FROM user_data;")

    #         for record in cur.fetchone():
    #             print(record)
    new_media(args[1], int(args[2]))


if __name__ == "__main__":
    main(*sys.argv)
