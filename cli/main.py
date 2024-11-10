#!/usr/bin/env python3


import psycopg
import argparse
import sys


DATABASE_NAME = "multimedia_db"
DATABASE_USER = "postgres"


def main(*args) -> None:
    with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM user_data;")

            for record in cur.fetchone():
                print(record)


if __name__ == "__main__":
    main(*sys.argv)
