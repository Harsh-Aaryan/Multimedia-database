#!/usr/bin/env python3


from constants import *
import ast
import psycopg
import random
import shlex
import sys
import time


def new_id(source_table: str) -> int:
    new_id = None

    with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
        with conn.cursor() as cur:
            while True:
                try:
                    new_id = random.randrange(POSTGRES_MAX_INTEGER_SIZE)

                    formatted_query = psycopg.sql.SQL("INSERT INTO {0} (id) VALUES ({1})")
                    formatted_query = formatted_query.format(
                        psycopg.sql.Identifier(source_table),
                        new_id
                    )

                    cur.execute(formatted_query.as_string())
                    break

                except psycopg.errors.UniqueViolation:
                    pass

    return new_id


def new_user(username: str, email: str, password: str) -> int:
    user_id = new_id("user_data")
    creation_time_posix = int(time.time())

    with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE user_data SET username = %s, email = %s, password = %s, access_level = %s WHERE id = %s;",
                (username, email, password, 2, user_id)
            )

    return user_id


def new_media(title: str, release_year: str) -> int:
    media_id = new_id("media")
    time_added_posix = int(time.time())

    with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE media SET title = %s, time_added_posix = %s, release_year = %s WHERE id = %s",
                (title, time_added_posix, int(release_year), media_id)
            )

    return media_id


def new_book(title: str, release_year: str, author: str, publisher: str, isbn: str) -> int:
    book_id = new_media(title, release_year)

    with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO book VALUES (%s, %s, %s, %s)",
                (book_id, author, publisher, isbn)
            )

    return book_id


def new_movie(title: str, release_year: str, director: str, publisher: str, genre: str, duration_seconds: str) -> int:
    movie_id = new_media(title, release_year)

    with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO movie VALUES (%s, %s, %s, %s, %s)",
                (movie_id, director, publisher, genre, int(duration_seconds))
            )

    return movie_id


def new_music(title: str, release_year: str, artist: str, album: str, genre: str, duration_seconds: str) -> int:
    music_id = new_media(title, release_year)

    with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO music VALUES (%s, %s, %s, %s, %s)",
                (music_id, artist, album, genre, int(duration_seconds))
            )

    return music_id


def main(*args) -> None:
    for a in args[1:]:
        values = {
            "table": a.split(":")[0],
            "tuple": ":".join(a.split(":")[1:]).split(";")
        }

        match values["table"]:
            case "user":
                print(new_user(*values["tuple"]))

            case "book":
                print(new_book(*values["tuple"]))

            case "movie":
                print(new_movie(*values["tuple"]))

            case "music":
                print(new_music(*values["tuple"]))

            case "media":
                print(new_media(*values["tuple"]))

            case _:
                print("<help>")


if __name__ == "__main__":
    main(*sys.argv)
