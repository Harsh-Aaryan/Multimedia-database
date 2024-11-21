#!/usr/bin/env python3
import getpass
import random
import sys
import time

import psycopg

RETURN_TIME_DAYS = 30
RETURN_TIME_SECONDS = 30 #60 * 60 * 24 * RETURN_TIME_DAYS

VIEWER_ACCESS_LEVEL = 3
USER_ACCESS_LEVEL = 2
ADMIN_ACCESS_LEVEL = 1
ROOT_ACCESS_LEVEL = 0

ADD_RETRIES = 20

TABLE_MAPPING = {
    "account": "full_user",
    "book": "full_book",
    "checked-out": "full_renting",
    "media": "media",
    "movie": "full_movie",
    "music": "full_music"
}

COLUMN_MAPPING = {
    "access-level": "access_level",
    "album": "album",
    "artist": "artist",
    "author": "author",
    "date-added": "time_added_posix",
    "date-checked-out": "start_time_posix",
    "date-due": "end_time_posix",
    "date-returned": "time_returned_posix",
    "director": "director",
    "duration-seconds": "duration_seconds",
    "email": "email",
    "genre": "genre",
    "id": "id",
    "isbn": "isbn",
    "media-id": "media_id",
    "overdue-media": "overdue_media",
    "password": "password",
    "publisher": "publisher",
    "release-year": "release_year",
    "title": "title",
    "user-id": "user_id",
    "username": "username"
}

USER_TABLE = "username\temail\taccess-level\toverdue-media"
MEDIA_TABLE = "id\tdate-added\ttitle\trelease-year"
BOOK_TABLE = f"{MEDIA_TABLE}\tauthor\tpublisher\tisbn"
MOVIE_TABLE = f"{MEDIA_TABLE}\tdirector\tpublisher\tgenre\tduration-seconds"
MUSIC_TABLE = f"{MEDIA_TABLE}\tartist\tpublisher\talbum\tgenre\tduration-seconds"
RENTING_TABLE = f"id\tdate-checked-out\tdate-due\ttime-returned\tusername\temail\tmedia-id\tdate-added\ttitle\trelease-year"

USER_WIDTH = 6
MEDIA_WIDTH = 4
BOOK_WIDTH = 7
MOVIE_WIDTH = 8
MUSIC_WIDTH = 9
RENTING_WIDTH = 11

COLUMNS = {
    USER_WIDTH: USER_TABLE,
    MEDIA_WIDTH: MEDIA_TABLE,
    BOOK_WIDTH: BOOK_TABLE,
    MOVIE_WIDTH: MOVIE_TABLE,
    MUSIC_WIDTH: MUSIC_TABLE,
    RENTING_WIDTH: RENTING_TABLE
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

HELP = {
    "ADD": f"""usage: {sys.argv[0]} [main options] add [<type>=<attributes>]...

add accounts and/or media to the database

types and attributes:
  account=<username>;<email>;<password>
  media=<title>;<release-year>
  book=<title>;<release-year>;<author>;<publisher>;<isbn>
  movie=<title>;<release-year>;<director>;<publisher>;<genre>;<duration>
  music=<title>;<release-year>;<artist>;<album>;<genre>;<duration-seconds>""",

    "CHECKOUT": f"""usage: {sys.argv[0]} [main options] checkout [options] <aliases> [<type>.
       <attribute><operator><value>]...

check out media from the database

options:
  -y, --yes                 skip user confirmation prompt
  -i, --intersection        use intersection of results instead of union of
                            results
  -s, --show-checked-out    show checked out media in results
  -a, --all                 show all overdue media; requires overdue and admin
                            account or higher

aliases:
  checked-out               search checked out media; requires -i
  overdue                   search overdue medial; requires -i

types, attributes, and value types:
  media.<id: int | title: str | release-year: int | date-added: int>
  book.<media attributes | author: str | publisher: str | isbn: str>
  movie.<media attributes | director: str | publisher: str | genre: str |
        duration-seconds: int>
  music.<media attributes | artist: str | album: str | genre: str |
        duration-seconds: int>
  checked-out.<id: int | date-checked-out: int | date-due: int | date-returned:
              int | account attributes | media-id: int | title: str |
              release-year: int | date-added: int>

operators:
  :                         search for substring; not case sensetive; applies
                            to str
  <                         search for less than; applies to int
  =                         search for exact match; applies to str and int
  >                         search for greater than; applies to int""",

    "MAIN": f"""usage: {sys.argv[0]} [options] <command> [<args>]

options:
      --help                display this help and exit
  -a, --all                 display all help and exit; requires --help
  -e, --email [email]       email to sign in with; not necessary with -u;
                            requires -p
  -u, --username [username]  username to sign in with; not necessary with -e;
                            requires -p
  -p, --password [password]  password to sign in with; required with -u and -e

commands:
  add                       add accounts and/or media to the database; requires
                            admin account or higher
  checkout                  checkout media from the database; requires user
                            account or higher
  remove                    remove accounts and/or media from the database;
                            requires user account or higher
  return                    return media to the database; requires user account
                            or higher
  search                    search accounts, media, and media status
  set                       change the value of an attribute of an account or
                            media""",

    "REMOVE": f"""usage: {sys.argv[0]} [main options] remove [options] <aliases> [<type>.
       <attribute><operator><value>]...

remove accounts and/or media from the database

options:
  -y, --yes                 skip user confirmation prompt
  -i, --intersection        use intersection of results instead of union of
                            results
  -s, --show-checked-out    show checked out media in results
  -a, --all                 show all overdue media; requires overdue and admin
                            account or higher

aliases:
  account                   search for signed in account
  checked-out               search checked out media; requires -i
  overdue                   search overdue medial; requires -i

types, attributes, and value types:
  account.<username: str | email: str | access-level: int | overdue-media: int>
  media.<id: int | title: str | release-year: int | date-added: int>
  book.<media attributes | author: str | publisher: str | isbn: str>
  movie.<media attributes | director: str | publisher: str | genre: str |
        duration-seconds: int>
  music.<media attributes | artist: str | album: str | genre: str |
        duration-seconds: int>
  checked-out.<id: int | date-checked-out: int | date-due: int | date-returned:
              int | account attributes | media-id: int | title: str |
              release-year: int | date-added: int>

operators:
  :                         search for substring; not case sensetive; applies
                            to str
  <                         search for less than; applies to int
  =                         search for exact match; applies to str and int
  >                         search for greater than; applies to int""",

    "RETURN": f"""usage: {sys.argv[0]} [main options] return [options] <aliases> [<type>.
       <attribute><operator><value>]...

return checked out media to the database; search -i is enabled

options:
  -y, --yes                 skip user confirmation prompt
  -s, --show-checked-out    show checked out media in results

aliases:
  overdue                   search overdue medial

types, attributes, and value types:
  media.<id: int | title: str | release-year: int | date-added: int>
  book.<media attributes | author: str | publisher: str | isbn: str>
  movie.<media attributes | director: str | publisher: str | genre: str |
        duration-seconds: int>
  music.<media attributes | artist: str | album: str | genre: str |
        duration-seconds: int>
  checked-out.<id: int | date-checked-out: int | date-due: int | date-returned:
              int | account attributes | media-id: int | title: str |
              release-year: int | date-added: int>

operators:
  :                         search for substring; not case sensetive; applies
                            to str
  <                         search for less than; applies to int
  =                         search for exact match; applies to str and int
  >                         search for greater than; applies to int""",

    "SEARCH": f"""usage: {sys.argv[0]} [main options] search [options] <aliases> [<type>.
       <attribute><operator><value>]...

options:
  -i, --intersection        use intersection of results instead of union of
                            results
  -s, --show-checked-out    show checked out media in results
  -a, --all                 show all overdue media; requires overdue and admin
                            account or higher

aliases:
  account                   search for signed in account
  checked-out               search checked out media; requires -i
  overdue                   search overdue medial; requires -i

types, attributes, and value types:
  account.<username: str | email: str | access-level: int | overdue-media: int>
  media.<id: int | title: str | release-year: int | date-added: int>
  book.<media attributes | author: str | publisher: str | isbn: str>
  movie.<media attributes | director: str | publisher: str | genre: str |
        duration-seconds: int>
  music.<media attributes | artist: str | album: str | genre: str |
        duration-seconds: int>
  checked-out.<id: int | date-checked-out: int | date-due: int | date-returned:
              int | account attributes | media-id: int | title: str |
              release-year: int | date-added: int>

operators:
  :                         search for substring; not case sensetive; applies
                            to str
  <                         search for less than; applies to int
  =                         search for exact match; applies to str and int
  >                         search for greater than; applies to int""",

    "SET": f"""usage: {sys.argv[0]} [main options] set [<type>.<attribute><operator>
       <value>]... [<new attribute>=<new value>;...]

set values of specific accounts or media; multiple values can be updated at
once, but only one account or media can be updated at a time

options:
  -y, --yes                 skip user confirmation prompt
  -i, --intersection        use intersection of results instead of union of
                            results
  -s, --show-checked-out    show checked out media in results
  -a, --all                 show all overdue media; requires overdue and admin
                            account or higher

aliases:
  checked-out               search checked out media; requires -i
  overdue                   search overdue medial; requires -i

types, attributes, and value types:
  account.<username: str | email: str | access-level: int | overdue-media: int>
  media.<id: int | title: str | release-year: int | date-added: int>
  book.<media attributes | author: str | publisher: str | isbn: str>
  movie.<media attributes | director: str | publisher: str | genre: str |
        duration-seconds: int>
  music.<media attributes | artist: str | album: str | genre: str |
        duration-seconds: int>
  checked-out.<id: int | date-checked-out: int | date-due: int | date-returned:
              int | account attributes | media-id: int | title: str |
              release-year: int | date-added: int>

operators:
  :                         search for substring; not case sensetive; applies
                            to str
  <                         search for less than; applies to int
  =                         search for exact match; applies to str and int
  >                         search for greater than; applies to int"""
}


def time_posix() -> int:
    return int(time.time())


def format_user_data(user_entry: tuple[any]) -> str:
    user_entry = [str(v) for v in user_entry[1:3] + user_entry[4:]]
    return "\t".join(user_entry)


def format_media(media_entry: tuple[any]) -> str:
    media_entry = [str(v) for v in media_entry]
    return "\t".join(media_entry)


def format_book(book_entry: tuple[any]) -> str:
    book_entry = [str(v) for v in book_entry]
    return "\t".join(book_entry)


def format_movie(movie_entry: tuple[any]) -> str:
    movie_entry = [str(v) for v in movie_entry]
    return "\t".join(movie_entry)


def format_music(music_entry: tuple[any]) -> str:
    music_entry = [str(v) for v in music_entry]
    return "\t".join(music_entry)


def format_renting(renting_entry: tuple[any]) -> str:
    renting_entry = [str(v) for v in renting_entry[:4] + renting_entry[5:]]
    return "\t".join(renting_entry)


def format_entry(entry: tuple[any]) -> str:
    match len(entry):
        case 6:
            return format_user_data(entry)

        case 4:
            return format_media(entry)

        case 7:
            return format_book(entry)

        case 8:
            return format_movie(entry)

        case 11:
            return format_renting(entry)


class Client:
    def __init__(self, cursor: psycopg.Cursor, account_id: int = -1, access_level: int = 3) -> None:
        self.cursor: psycopg.Cursor = cursor
        self.account_id: int = account_id
        self.access_level: int = access_level

    def check_permissions(self, required_access_level: int) -> None:
        if self.access_level > required_access_level:
            print(f"Permission denied (Requires access level {required_access_level})")
            exit(1)

    def new_id(self, source_table: str) -> int:
        for _ in range(ADD_RETRIES):
            try:
                new_id = random.randrange(POSTGRES_MAX_INTEGER_SIZE + 1)

                formatted_query = psycopg.sql.SQL("INSERT INTO {0} (id) VALUES ({1});")
                formatted_query = formatted_query.format(
                    psycopg.sql.Identifier(source_table),
                    new_id
                )

                self.cursor.execute(formatted_query.as_string())
                return new_id

            except psycopg.errors.UniqueViolation:
                pass
            except psycopg.errors.InFailedSqlTransaction:
                pass

        for i in range(POSTGRES_MAX_INTEGER_SIZE + 1):
            try:
                formatted_query = psycopg.sql.SQL("INSERT INTO {0} (id) VALUES ({1});")
                formatted_query = formatted_query.format(
                    psycopg.sql.Identifier(source_table),
                    i
                )

                self.cursor.execute(formatted_query.as_string())
                return i

            except psycopg.errors.UniqueViolation:
                pass
            except psycopg.errors.InFailedSqlTransaction:
                pass

        print("Out of media slots")
        exit(1)

    def new_user(self, username: str, email: str, password: str) -> int:
        user_id = self.new_id("user_data")
        creation_time_posix = time_posix()

        self.cursor.execute(
            "UPDATE user_data SET username = %s, email = %s, password = %s, access_level = %s WHERE id = %s;",
            (username, email, password, 2, user_id)
        )

        return user_id

    def new_media(self, title: str, release_year: str) -> int:
        self.check_permissions(ADMIN_ACCESS_LEVEL)

        media_id = self.new_id("media")
        time_added_posix = time_posix()

        self.cursor.execute(
            "UPDATE media SET time_added_posix = %s, title = %s, release_year = %s WHERE id = %s;",
            (time_added_posix, title, int(release_year), media_id)
        )

        return media_id

    def new_book(self, title: str, release_year: str, author: str, publisher: str, isbn: str) -> int:
        book_id = self.new_media(title, release_year)

        self.cursor.execute(
            "INSERT INTO book VALUES (%s, %s, %s, %s);",
            (book_id, author, publisher, isbn)
        )

        return book_id

    def new_movie(self, title: str, release_year: str, director: str, publisher: str, genre: str,
                  duration_seconds: str) -> int:
        movie_id = self.new_media(title, release_year)

        self.cursor.execute(
            "INSERT INTO movie VALUES (%s, %s, %s, %s, %s);",
            (movie_id, director, publisher, genre, int(duration_seconds))
        )

        return movie_id

    def new_music(self, title: str, release_year: str, artist: str, album: str, genre: str,
                  duration_seconds: str) -> int:
        music_id = self.new_media(title, release_year)

        self.cursor.execute(
            "INSERT INTO music VALUES (%s, %s, %s, %s, %s);",
            (music_id, artist, album, genre, int(duration_seconds))
        )

        return music_id

    def add(self, *args: str) -> None:
        if args[1] == "--help":
            print(HELP["ADD"])
            exit()

        for a in args[1:]:
            values = {
                "table": a[:a.index("=")],
                "tuple": a[a.index("=") + 1:].split(";")
            }

            values["table"] = TABLE_MAPPING[values["table"]]

            match values["table"]:
                case "user_data":
                    print(self.new_user(*values["tuple"]), *[repr(v) for v in values["tuple"]])

                case "full_book":
                    print(self.new_book(*values["tuple"]), *[repr(v) for v in values["tuple"]])

                case "full_movie":
                    print(self.new_movie(*values["tuple"]), *[repr(v) for v in values["tuple"]])

                case "full_music":
                    print(self.new_music(*values["tuple"]), *[repr(v) for v in values["tuple"]])

                case "media":
                    print(self.new_media(*values["tuple"]), *[repr(v) for v in values["tuple"]])

    def query_database(self, table: str, column: str, operator: str, query: str, show_checked_out: bool = False) -> \
            list[tuple]:
        formatted_query = None
        match operator:
            case ":":
                formatted_query = psycopg.sql.SQL("SELECT * FROM {0} AS m WHERE LOWER ({1}) LIKE {2};")
                formatted_query = formatted_query.format(
                    psycopg.sql.Identifier(table),
                    psycopg.sql.Identifier(column),
                    f"%{query.lower()}%"
                )

            case "<":
                formatted_query = psycopg.sql.SQL("SELECT * FROM {0} AS m WHERE {1} < {2};")
                formatted_query = formatted_query.format(
                    psycopg.sql.Identifier(table),
                    psycopg.sql.Identifier(column),
                    int(query)
                )

            case "=":
                formatted_query = psycopg.sql.SQL("SELECT * FROM {0} AS m WHERE {1} = {2};")
                formatted_query = formatted_query.format(
                    psycopg.sql.Identifier(table),
                    psycopg.sql.Identifier(column),
                    query
                )

            case ">":
                formatted_query = psycopg.sql.SQL("SELECT * FROM {0} AS m WHERE {1} > {2};")
                formatted_query = formatted_query.format(
                    psycopg.sql.Identifier(table),
                    psycopg.sql.Identifier(column),
                    int(query)
                )

        sql_command = formatted_query.as_string()

        if not show_checked_out and table in ["media", "full_book", "full_movie", "full_music"]:
            sql_command = f"{sql_command[:-1]} AND NOT EXISTS (SELECT r.media_id FROM renting AS r WHERE m.id = r.media_id AND r.time_returned_posix = 9223372036854775807);"

        self.cursor.execute(sql_command)

        return self.cursor.fetchall()

    def formatted_search(self, *queries: str) -> list[tuple]:
        queries = list(queries)

        output = set()

        if "account" in queries:
            queries[queries.index("account")] = f"account.id={self.account_id}"

        if "checked-out" in queries:
            queries[queries.index("checked-out")] = "-i"
            queries.append(f"checked-out.user-id={self.account_id}")
            queries.append(f"checked-out.date-returned={POSTGRES_MAX_BIGINT_SIZE}")

        if "overdue" in queries:
            queries[queries.index("overdue")] = "-i"
            queries += [
                f"checked-out.date-returned={POSTGRES_MAX_BIGINT_SIZE}",
                f"checked-out.date-due<{time_posix()}"
            ]

            show_all = False
            show_all_index = queries.index("--all") if "--all" in queries else -1
            show_all_index = queries.index("-a") if show_all_index == -1 and "-a" in queries else show_all_index

            if show_all_index == -1:
                queries.append(f"checked-out.user-id={self.account_id}")

            else:
                del queries[show_all_index]
                self.check_permissions(ADMIN_ACCESS_LEVEL)

        intersection = False
        intersection_index = queries.index("--intersection") if "--intersection" in queries else -1
        intersection_index = queries.index("-i") if intersection_index == -1 and "-i" in queries else intersection_index

        if intersection_index != -1:
            intersection = True
            del queries[intersection_index]

        show_checked_out = False
        show_checked_out_index = queries.index("--show-checked-out") if "--show-checked-out" in queries else -1
        show_checked_out_index = queries.index(
            "-s") if show_checked_out_index == -1 and "-s" in queries else show_checked_out_index

        if show_checked_out_index != -1:
            show_checked_out = True
            del queries[show_checked_out_index]

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

            if ((values["table"] == "full_user" and values["column"] == "id") or values["column"] == "user_id") and \
                    values["query"] != str(self.account_id):
                print("Permission denied. Cannot search for other users.")
                exit(1)

            if values["column"] == "password":
                print("Permission denied")
                exit(1)

            if values["table"] == "full_renting":
                self.check_permissions(ADMIN_ACCESS_LEVEL)

            result = set(self.query_database(values["table"], values["column"], values["operation"], values["query"],
                                             show_checked_out))

            if output != set() and intersection:
                output = output.intersection(result)
            else:
                output = output.union(result)

        return sorted(list(output))

    def search(self, *args: str) -> None:
        if args[1] == "--help":
            print(HELP["SEARCH"])
            exit()

        results = self.formatted_search(*args[1:])

        previous_len = 0
        for result in results:
            if len(result) != previous_len:
                print(COLUMNS[len(result)])
                previous_len = len(result)

            print(format_entry(result))

    def checkout(self, *args: str) -> None:
        args = list(args)

        if args[1] == "--help":
            print(HELP["CHECKOUT"])
            exit()

        autoconfirm = False
        autoconfirm_index = args.index("--yes") if "--yes" in args else -1
        autoconfirm_index = args.index("-y") if autoconfirm_index == -1 and "-y" in args else autoconfirm_index

        if autoconfirm_index != -1:
            autoconfirm = True
            del args[autoconfirm_index]

        checkout_time = time_posix()

        checkout_queue = self.formatted_search(*args[1:])

        previous_len = 0
        for result in checkout_queue:
            if len(result) != previous_len:
                print(COLUMNS[len(result)])
                previous_len = len(result)

            print(format_entry(result))

        if not autoconfirm and input("Do you want to check out this media [y/n] ").casefold() not in ("y", "yes"):
            exit(1)

        for result in checkout_queue:
            if len(result) == USER_WIDTH:
                print(f"Can't checkout account")
                continue

            renting_id = self.new_id("renting")

            self.cursor.execute(
                "UPDATE renting SET user_id = %s, media_id = %s, start_time_posix = %s, end_time_posix = %s, time_returned_posix = %s WHERE id = %s;",
                (self.account_id, result[0], checkout_time, checkout_time + RETURN_TIME_SECONDS,
                 POSTGRES_MAX_BIGINT_SIZE, renting_id)
            )

    def remove(self, *args: str) -> None:
        args = list(args)

        if args[1] == "--help":
            print(HELP["REMOVE"])
            exit()

        autoconfirm = False
        autoconfirm_index = args.index("--yes") if "--yes" in args else -1
        autoconfirm_index = args.index("-y") if autoconfirm_index == -1 and "-y" in args else autoconfirm_index

        if autoconfirm_index != -1:
            autoconfirm = True
            del args[autoconfirm_index]

        if args != ["account"]:
            self.check_permissions(ADMIN_ACCESS_LEVEL)

        deletion_queue = self.formatted_search(*args[1:], "--show-checked-out")

        previous_len = 0
        for result in deletion_queue:
            if len(result) != previous_len:
                print(COLUMNS[len(result)])
                previous_len = len(result)

            print(format_entry(result))

        if not autoconfirm and input("Do you want to remove these entries? [y/n] ").casefold() not in ("y", "yes"):
            exit(1)

        for result in deletion_queue:
            if len(result) == 5:
                self.cursor.execute("DELETE FROM user_data WHERE id = %s;", (result[0],))

            else:
                self.cursor.execute("DELETE FROM media WHERE id = %s;", (result[0],))

    def return_media(self, *args: str) -> None:
        args = list(args)

        if args[1] == "--help":
            print(HELP["RETURN"])
            exit()

        autoconfirm = False
        autoconfirm_index = args.index("--yes") if "--yes" in args else -1
        autoconfirm_index = args.index("-y") if autoconfirm_index == -1 and "-y" in args else autoconfirm_index

        if autoconfirm_index != -1:
            autoconfirm = True
            del args[autoconfirm_index]

        return_time = time_posix()

        return_queue = self.formatted_search(*args[1:], "checked-out")

        previous_len = 0
        for result in return_queue:
            if len(result) != previous_len:
                print(COLUMNS[len(result)])
                previous_len = len(result)

            print(format_entry(result))

        if not autoconfirm and input("Do you want to return this media [y/n] ").casefold() not in ("y", "yes"):
            exit(1)

        for result in return_queue:
            self.cursor.execute(
                "UPDATE renting SET time_returned_posix = %s WHERE id = %s;",
                (return_time, result[0])
            )

    def set_value(self, operations: str, *args: str) -> None:
        args = list(args)

        if args[1] == "--help":
            print(HELP["SET"])
            exit()

        autoconfirm = False
        autoconfirm_index = args.index("--yes") if "--yes" in args else -1
        autoconfirm_index = args.index("-y") if autoconfirm_index == -1 and "-y" in args else autoconfirm_index

        if autoconfirm_index != -1:
            autoconfirm = True
            del args[autoconfirm_index]

        if args != ["account"] and sorted(args) != ["--intersection", "account"] and sorted(args) != ["-i",
                                                                                                      "account"] and sorted(
            args) != ["--intersection", "-i", "account"]:
            self.check_permissions(ADMIN_ACCESS_LEVEL)

        selected_tuple = self.formatted_search(*args[1:-1], "--show-checked-out")

        if len(selected_tuple) > 1:
            print("More than one entry selected")
            exit(1)

        selected_tuple = selected_tuple[0]

        print(format_entry(selected_tuple))

        if not autoconfirm and input("Do you want to modify this entry [y/n] ").casefold() not in ("y", "yes"):
            exit(1)

        for o in operations.split(";"):
            values = {
                "table": args[1][:args[1].index(".")],
                "column": operations[:operations.index("=")],
                "value": operations[operations.index("=") + 1:]
            }

            values["table"] = TABLE_MAPPING[values["table"]]
            values["column"] = COLUMN_MAPPING[values["column"]]

            if values["column"] == "overdue_media" or values["column"] in ["id", "user_id"]:
                print(f"Unable to modify {operations[:operations.index("=")]}")
                exit(1)

            formatted_query = psycopg.sql.SQL("UPDATE {0} SET {1} = {2} WHERE id = {3};")
            formatted_query = formatted_query.format(
                psycopg.sql.Identifier(values["table"]),
                psycopg.sql.Identifier(values["column"]),
                values["value"],
                selected_tuple[0]
            )

            self.cursor.execute(formatted_query.as_string())

    def main(self, *args: str) -> None:
        try:
            match args[1]:
                case "add":
                    self.add(*args[1:])
                    return

                case "checkout":
                    self.checkout(*args[1:])
                    return

                case "remove":
                    self.remove(*args[1:])
                    return

                case "return":
                    self.return_media(*args[1:])
                    return

                case "search":
                    self.search(*args[1:])
                    return

                case "set":
                    self.set_value(args[-1], *args[1:])
                    return

                case _:
                    print(f"Unrecognized command {repr(args[1])}")
                    return

        except IndexError:
            pass
        except KeyError:
            pass
        except psycopg.errors.InvalidTextRepresentation:
            pass
        except psycopg.errors.UndefinedFunction:
            pass
        except ValueError:
            pass

        print(f"Invalid input\nTry '{args[0]} {args[1]} --help' for more information.")
        exit(1)


def check_login(cursor: psycopg.Cursor, args: list[str]) -> any:
    args_index = {
        "username": args.index("--username") if "--username" in args else -1,
        "email": args.index("--email") if "--email" in args else -1,
        "password": args.index("--password") if "--password" in args else -1
    }
    args_index["username"] = args.index("-u") if "-u" in args and args_index["username"] == -1 else args_index[
        "username"]
    args_index["email"] = args.index("-e") if "-e" in args and args_index["email"] == -1 else args_index["email"]
    args_index["password"] = args.index("-p") if "-p" in args and args_index["password"] == -1 else args_index[
        "password"]

    if args_index["username"] == -1 and args_index["email"] == -1 and args_index["password"] == -1:
        return

    if (args_index["username"] != -1 or args_index["email"] != -1) and args_index["password"] == -1:
        print("Invalid login. Missing --password or -p")
        exit(1)


    cursor.execute("SELECT * FROM user_data WHERE (username = %s OR email = %s) AND password = %s;",
                   (args[args_index["username"] + 1], args[args_index["email"] + 1], args[args_index["password"] + 1])
                   )
    account = cursor.fetchone()

    if account is None:
        print("Invalid login")
        exit(1)

    args_indicies = list()
    for _, v in args_index.items():
        if v == -1:
            continue

        args_indicies.append(v)

    for i in reversed(sorted(args_indicies)):
        del args[i + 1]
        del args[i]

    return account


def main(*args: str) -> None:
    args = list(args)

    invalid_message = f"Invalid input\nTry '{args[0]} --help' for more information."

    if len(args) <= 1:
        print(invalid_message)
        exit(1)

    if args[1] == "--help":
        print(HELP["MAIN"])

        if len(args) >= 3 and args[2] in ["-a", "--all"]:
            for k in HELP:
                if k == "MAIN":
                    continue

                print(HELP[k])

                if k != "SET":
                    print()

        exit()

    try:
        with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER}") as conn:
            with conn.cursor() as cur:

                account = check_login(cur, args)

                if account is not None:
                    client = Client(cur, account[0], account[4])

                else:
                    client = Client(cur)

                if len(args) <= 1:
                    print(invalid_message)
                    exit(1)

                client.main(*args)

                conn.commit()
    except psycopg.errors.OperationalError as e:
        if "no password supplied" in str(e):
            db_password = getpass.getpass("PostgreSQL Password: ")
            with psycopg.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER} password={db_password}") as conn:
                with conn.cursor() as cur:

                    account = check_login(cur, args)

                    if account is not None:
                        client = Client(cur, account[0], account[4])

                    else:
                        client = Client(cur)

                    if len(args) <= 1:
                        print(invalid_message)
                        exit(1)

                    client.main(*args)

                    conn.commit()


if __name__ == "__main__":
    main(*sys.argv)
