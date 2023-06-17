import os
from urllib.parse import urlparse

import psycopg2

from .base import ASSISTANTS, Assistant


def get_connection(database_url):
    result = urlparse(database_url)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port
    return psycopg2.connect(
        database=database, user=username, password=password, host=hostname, port=port
    )


def get_database_information():
    database_url = os.environ.get("DATABASE_URL")
    connection = get_connection(database_url)
    cur = connection.cursor()
    cur.execute("SELECT tablename FROM pg_catalog.pg_tables ORDER BY tablename;")
    output = cur.fetchall()
    tables = [t[0] for t in output if not t[0].startswith("pg_")]

    response = ""
    for t in tables:
        cur.execute(
            f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{t}';"
        )
        output = cur.fetchall()
        response += f"\ntable: {t}\n______\ncolumn_name, data_type\n"

        for c in output:
            response += f"{c[0]},{c[1]}\n"

    connection.close()

    return response


def postgress_prompt():
    messages = [
        {
            "role": "system",
            "content": "You're are the assisent of the developer for creating sql queries for a specific postgres database. The developer will ask how do a certain action and you will return a valid sql query",
        },
        {
            "role": "system",
            "content": f"This is table information of the database\n ```{get_database_information()}```",
        },
    ]

    return messages


ASSISTANTS["postgres"] = Assistant(
    "🐘 ",
    "The postgres assistant",
    postgress_prompt,
)
