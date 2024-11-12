#!/usr/bin/env python3


from constants import *
import psycopg
import search
import sys


def main(*args) -> None:
    deletion_queue = [id[0] for id in search.search(args[1], args[2], args[3], True)]

    with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
        with conn.cursor() as cur:
            for id in deletion_queue:
                cur.execute(f"DELETE FROM media WHERE id = %s;", (id,))


if __name__ == "__main__":
    main(*sys.argv)
