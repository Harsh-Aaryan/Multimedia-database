#!/usr/bin/env python3


from constants import *
import psycopg
import sys


def search(table: str, column: str, query: str, return_only_id: bool=False) -> list[tuple]:
    query = query.lower()

    formatted_query = None

    if return_only_id:
        formatted_query = psycopg.sql.SQL("SELECT id FROM {0} WHERE LOWER ({1}) LIKE {2}")
        formatted_query = formatted_query.format(
            psycopg.sql.Identifier(table),
            psycopg.sql.Identifier(column),
            f"%%{query}%%"
        )

    else:
        formatted_query = psycopg.sql.SQL("SELECT * FROM {0} WHERE LOWER ({1}) LIKE {2}")
        formatted_query = formatted_query.format(
            psycopg.sql.Identifier(table),
            psycopg.sql.Identifier(column),
            f"%%{query}%%"
        )


    with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
        with conn.cursor() as cur:
            cur.execute(formatted_query.as_string())

            return cur.fetchall()


def main(*args) -> None:
    print(search(*args[1:]))


if __name__ == "__main__":
    main(*sys.argv)
