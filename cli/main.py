#!/usr/bin/env python3


import argparse
import json
import psycopg
import random
import sys
import time


RETURN_TIME_DAYS = 30
RETURN_TIME_SECONDS = 60 * 60 * 24 * RETURN_TIME_DAYS

TABLE_MAPPING = {
    "account": "user_data",
    "book": "full_book",
    "checked-out": "full_renting",
    "media": "media",
    "movie": "full_movie",
    "music": "full_music"
}

COLUMN_MAPPING = {
    "album": "album",
    "artist": "artist",
    "author": "author",
    "date-added": "time_added_posix",
    "date-due": "end_time_posix",
    "date-returned": "time_returned_posix",
    "director": "director",
    "duration": "duration_seconds",
    "email": "email",
    "genre": "genre",
    "id": "id",
    "isbn": "isbn",
    "password": "password",
    "publisher": "publisher",
    "release-year": "release_year",
    "title": "title",
    "user-id": "user_id",
    "username": "username"
}

OPERATORS = [   #   Python; SQL
    ":",        #   in      like
    "<",        #   <       <
    "=",        #   ==      =
    ">"         #   >       >
]

DATABASE_NAME = "multimedia_db"
DATABASE_USER = "postgres"
POSTGRES_MAX_INTEGER_SIZE = 2147483647
POSTGRES_MAX_BIGINT_SIZE = 9223372036854775807


def time_posix() -> int:
    return int(time.time())


class Client:
    def __init__(self, account_id: int=-1, access_level: int=3) -> None:
        self.account_id: int = account_id
        self.access_level: int = access_level


    def new_id(self, source_table: str) -> int:
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


    def new_user(self, username: str, email: str, password: str) -> int:
        user_id = self.new_id("user_data")
        creation_time_posix = time_posix()

        with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE user_data SET username = %s, email = %s, password = %s, access_level = %s WHERE id = %s;",
                    (username, email, password, 2, user_id)
                )

        return user_id


    def new_media(self, title: str, release_year: str) -> int:
        media_id = self.new_id("media")
        time_added_posix = time_posix()

        with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE media SET time_added_posix = %s, title = %s, release_year = %s WHERE id = %s;",
                    (time_added_posix, title, int(release_year), media_id)
                )

        return media_id


    def new_book(self, title: str, release_year: str, author: str, publisher: str, isbn: str) -> int:
        book_id = self.new_media(title, release_year)

        with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO book VALUES (%s, %s, %s, %s)",
                    (book_id, author, publisher, isbn)
                )

        return book_id


    def new_movie(self, title: str, release_year: str, director: str, publisher: str, genre: str, duration_seconds: str) -> int:
        movie_id = self.new_media(title, release_year)

        with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO movie VALUES (%s, %s, %s, %s, %s)",
                    (movie_id, director, publisher, genre, int(duration_seconds))
                )

        return movie_id


    def new_music(self, title: str, release_year: str, artist: str, album: str, genre: str, duration_seconds: str) -> int:
        music_id = self.new_media(title, release_year)

        with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO music VALUES (%s, %s, %s, %s, %s)",
                    (music_id, artist, album, genre, int(duration_seconds))
                )

        return music_id


    def add(self, *args: str) -> None:
        for a in args[1:]:
            values = {
                "table": a[:a.index("=")],
                "tuple": a[a.index("=") + 1:].split(";")
            }

            values["table"] = TABLE_MAPPING[values["table"]]

            match values["table"]:
                case "user_data":
                    print(self.new_user(*values["tuple"]), *[repr(v) for v in values["tuple"]])

                case "book":
                    print(self.new_book(*values["tuple"]), *[repr(v) for v in values["tuple"]])

                case "movie":
                    print(self.new_movie(*values["tuple"]), *[repr(v) for v in values["tuple"]])

                case "music":
                    print(self.new_music(*values["tuple"]), *[repr(v) for v in values["tuple"]])

                case "media":
                    print(self.new_media(*values["tuple"]), *[repr(v) for v in values["tuple"]])

                case _:
                    print("<help>")


    def query_database(self, table: str, column: str, operator: str, query: str) -> list[tuple]:
        formatted_query = None
        match operator:
            case ":":
                formatted_query = psycopg.sql.SQL("SELECT * FROM {0} WHERE LOWER ({1}) LIKE {2};")
                formatted_query = formatted_query.format(
                    psycopg.sql.Identifier(table),
                    psycopg.sql.Identifier(column),
                    f"%{query.lower()}%"
                )

            case "<":
                formatted_query = psycopg.sql.SQL("SELECT * FROM {0} WHERE {1} < {2};")
                formatted_query = formatted_query.format(
                    psycopg.sql.Identifier(table),
                    psycopg.sql.Identifier(column),
                    int(query)
                )

            case "=":
                formatted_query = psycopg.sql.SQL("SELECT * FROM {0} WHERE {1} = {2};")
                formatted_query = formatted_query.format(
                    psycopg.sql.Identifier(table),
                    psycopg.sql.Identifier(column),
                    query
                )

            case ">":
                formatted_query = psycopg.sql.SQL("SELECT * FROM {0} WHERE {1} > {2};")
                formatted_query = formatted_query.format(
                    psycopg.sql.Identifier(table),
                    psycopg.sql.Identifier(column),
                    int(query)
                )

        with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
            with conn.cursor() as cur:
                cur.execute(formatted_query.as_string())

                return cur.fetchall()


    def formatted_search(self, *queries: str) -> list[tuple]:
        queries = list(queries)

        output = set()

        if "checked-out" in queries:
            queries[queries.index("checked-out")] = f"checked-out.user-id={self.account_id}"

        if "overdue" in queries:
            queries[queries.index("overdue")] = "-i"
            queries += [
                f"checked-out.user-id={self.account_id}",
                f"checked-out.date-returned={POSTGRES_MAX_BIGINT_SIZE}",
                f"checked-out.date-returned={POSTGRES_MAX_BIGINT_SIZE}",
                f"checked-out.date-due<{time_posix()}"
            ]

        intersection = False
        if "-i" in queries:
            intersection = True
            del queries[queries.index("-i")]

        for query in queries:
            operator_index = min([query.find(o) for o in OPERATORS if query.find(o) != -1])
            operator = query[operator_index]

            values = {
                "table": query[:query.index(".")],
                "column": query[query.index(".") + 1:operator_index],
                "operation": operator,
                "query": query[operator_index + 1:]
            }

            values["table"] = TABLE_MAPPING[values["table"]]
            values["column"] = COLUMN_MAPPING[values["column"]]

            result = set(self.query_database(values["table"], values["column"], values["operation"], values["query"]))

            if output != set() and intersection:
                output = output.intersection(result)
            else:
                output = output.union(result)

        return sorted(list(output))


    def search(self, *args: str) -> None:
        for result in self.formatted_search(*args[1:]):
            print(result)


    def checkout(self, *args: str) -> None:
        checkout_time = time_posix()

        checkout_queue = self.formatted_search(*args[1:])

        for i, result in enumerate(checkout_queue):
            print(f"{i}\t{result}")

        if input("Do you want to check out this media [y/n] ") != "y":
            exit(1)

        with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
            with conn.cursor() as cur:
                for result in checkout_queue:
                    renting_id = self.new_id("renting")

                    cur.execute(
                        "UPDATE renting SET user_id = %s, media_id = %s, start_time_posix = %s, end_time_posix = %s, time_returned_posix = %s WHERE id = %s;",
                        (self.account_id, result[0], checkout_time, checkout_time + RETURN_TIME_SECONDS, POSTGRES_MAX_BIGINT_SIZE, renting_id)
                    )


    def remove(self, *args: str) -> None:
        deletion_queue = self.formatted_search(*args[1:])

        for result in deletion_queue:
            print(result)

        if input("Do you want to remove this media? [y/n] ") != "y":
            exit(1)

        with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
            with conn.cursor() as cur:
                for result in deletion_queue:
                    cur.execute("DELETE FROM media WHERE id = %s;", (result[0],))


    def return_media(self, *args: str) -> None:
        return_time = time_posix()

        return_queue = self.formatted_search("checked-out", *args[1:])

        for i, result in enumerate(return_queue):
            print(f"{i}\t{result}")

        if input("Do you want to return this media [y/n] ") != "y":
            exit(1)

        with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
            with conn.cursor() as cur:
                for result in return_queue:
                    renting_id = self.new_id("renting")

                    cur.execute(
                        "UPDATE renting SET time_returned_posix = %s WHERE id = %s;",
                        (return_time, renting_id)
                    )


    def set_value(self, operations: str, *args: str) -> None:
        selected_tuple = self.formatted_search(*args[1:-1])

        if len(selected_tuple) > 1:
            exit(1)

        selected_tuple = selected_tuple[0]

        print(selected_tuple)

        if input("Do you want to modify this tuple [y/n] ") != "y":
            exit(1)

        for o in operations.split(";"):
            values = {
                "table": args[1][:args[1].index(".")],
                "column": operations[:operations.index("=")],
                "value": operations[operations.index("=") + 1:]
            }

            values["table"] = TABLE_MAPPING[values["table"]]
            values["column"] = COLUMN_MAPPING[values["column"]]
            print(values)
            with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
                with conn.cursor() as cur:
                    formatted_query = psycopg.sql.SQL("UPDATE {0} SET {1} = {2} WHERE id = {3};")
                    formatted_query = formatted_query.format(
                        psycopg.sql.Identifier(values["table"]),
                        psycopg.sql.Identifier(values["column"]),
                        values["value"],
                        selected_tuple[0]
                    )

                    cur.execute(formatted_query.as_string())


    def main(self, *args: str) -> None:
        match args[1]:
            case "add":
                self.add(*args[1:])

            case "checkout":
                self.checkout(*args[1:])

            case "remove":
                self.remove(*args[1:])

            case "return":
                self.return_media(*args[1:])

            case "search":
                self.search(*args[1:])

            case "set":
                self.set_value(args[-1], *args[1:])


def main(*args: str) -> None:
    args = list(args)

    login = False

    username = None
    email = None
    account = None
    password = None
    if "--username" in args:
        username_index = args.index("--username")
        username = args[username_index + 1]
        del args[username_index + 1]
        del args[username_index]

        with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM user_data WHERE username = %s;", (username,))

                account = cur.fetchone()

    elif "--email" in args:
        email_index = args.index("--email")
        email = args[email_index + 1]
        del args[email_index + 1]
        del args[email_index]

        with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM user_data WHERE email = %s;", (email,))

                account = cur.fetchone()

    if account != None and "--password" in args:
        password_index = args.index("--password")
        password = args[password_index + 1]
        del args[password_index + 1]
        del args[password_index]

        login = password == account[3]

    client = None
    if login:
        client = Client(account[0], account[4])

    elif username != None or email != None or password != None:
        print("Invalid login")
        exit(1)

    else:
        client = Client()

    client.main(*args)


if __name__ == "__main__":
    main(*sys.argv)
