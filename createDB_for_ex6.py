import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

connection = psycopg2.connect("postgresql://postgres:1234@localhost:5432")
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()
table_name = "ex6"

cursor.execute("SELECT 1 FROM pg_database WHERE datname='jokes'")
if cursor.fetchone() is None:
    cursor.execute(f"""CREATE DATABASE jokes""")

    connection = psycopg2.connect("postgresql://postgres:1234@localhost:5432/jokes")
    cursor = connection.cursor()
    query = f'''CREATE TABLE {table_name}(
           id SERIAL PRIMARY KEY,
            category TEXT,
           joke TEXT
        )'''
    cursor.execute(query)