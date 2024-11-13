#!/usr/bin/env python3


from constants import *
import psycopg
import search
import sys


def main(*args) -> None:
    deletion_queue = search.formatted_search(args[1])

    for result in deletion_queue:
        print(result)

    if input("Do you want to remove this media? [y/n] ") != "y":
        return

    with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
        with conn.cursor() as cur:
            for result in deletion_queue:
                cur.execute("DELETE FROM media WHERE id = %s;", (result[0],))


if __name__ == "__main__":
    main(*sys.argv)
