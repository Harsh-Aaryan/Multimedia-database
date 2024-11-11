#!/usr/bin/env python3


from constants import *
import psycopg
import random
import sys
import time


def new_id(source_table: str) -> int:
    with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM %s;", (source_table))

            existing_ids = [row[0] for row in cur.fetchall()]

    new_id = None
    while new_id == None or new_id in existing_ids:
        new_id = random.randrange(POSTGRES_MAX_INTEGER_SIZE)

    return new_id


def new_user(username: str, email: str, password: str) -> int:
    user_id = new_id("user_data")
    creation_time_posix = int(time.time())

    with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO user_data VALUES (%s, %s, %s, %s)",
                (user_id, username, email, password, 2)
            )

    return user_id


def new_media(title: str, release_year: str) -> int:
    media_id = new_id("media")
    creation_time_posix = int(time.time())

    with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO media VALUES (%s, %s, %s, %s)",
                (media_id, title, creation_time_posix, int(release_year))
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
    match args[1]:
        case "book":
            print(new_book(*args[2:]))

        case "movie":
            print(new_movie(*args[2:]))

        case "music":
            print(new_music(*args[2:]))

        case "media":
            print(new_media(*args[1:]))

        case _:
            print("<help>")


if __name__ == "__main__":
    main(*sys.argv)
