#!/usr/bin/env python3


from constants import *
import psycopg
import sys


def _search(table: str, column: str, operator: str, query: str) -> list[tuple]:
    query = query.lower()

    formatted_query = None
    match operator:
        case ":":
            formatted_query = psycopg.sql.SQL("SELECT * FROM {0} WHERE LOWER ({1}) LIKE {2};")
            formatted_query = formatted_query.format(
                psycopg.sql.Identifier(table),
                psycopg.sql.Identifier(column),
                f"%{query}%"
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


def formatted_search(query: str) -> list[tuple]:
    operator_index = min(*[query.find(o) * -1 for o in OPERATORS]) * -1
    operator = query[operator_index]

    values = {
        "table": query[:query.index(".")],
        "column": query[query.index(".") + 1:operator_index],
        "operation": operator,
        "query": query[operator_index + 1:]
    }

    values["table"] = TABLE_MAPPING[values["table"]]

    return _search(values["table"], values["column"], values["operation"], values["query"])


def main(*args) -> None:
    print(formatted_search(*args[1:]))


if __name__ == "__main__":
    main(*sys.argv)
