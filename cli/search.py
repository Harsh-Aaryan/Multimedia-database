#!/usr/bin/env python3


from constants import *
import psycopg
import sys


# ./search.py $table $field $value
def main(*args) -> None:
    with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {args[1]} WHERE {args[2]} = %s;", (args[3],))

            print(cur.fetchall())


if __name__ == "__main__":
    main(*sys.argv)
