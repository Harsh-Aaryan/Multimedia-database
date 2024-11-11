#!/usr/bin/env python3


from constants import *
import psycopg
import sys


def search(table: str, column: str, value: str, output_columns: str="*") -> list[tuple]:
    with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT {output_columns} FROM {table} WHERE {column} = %s;", (value,))

            return cur.fetchall()


# ./search.py $table $field $value
def main(*args) -> None:
    print(search(*args[1:]))


if __name__ == "__main__":
    main(*sys.argv)
