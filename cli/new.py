#!/usr/bin/env python3


from constants import *
import psycopg
import random
import sys
import time


def new_media_id() -> int:
    with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM media;")

            existing_ids = [row[0] for row in cur.fetchall()]

    new_id = None
    while new_id == None or new_id in existing_ids:
        new_id = random.randrange(POSTGRES_MAX_INTEGER_SIZE)

    return new_id


def new_media(title: str, release_year: int) -> int:
    media_id = new_media_id()
    creation_time_posix = int(time.time())

    with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO media VALUES (%s, %s, %s, %s)",
                (media_id, title, creation_time_posix, release_year)
            )

    return media_id


def main(*args) -> None:
    print(new_media(args[1], args[2]))


if __name__ == "__main__":
    main(*sys.argv)
