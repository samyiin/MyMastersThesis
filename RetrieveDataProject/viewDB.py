import pandas as pd

import sqlite3


def view_table(table_name):
    conn = sqlite3.connect('data.db')
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    conn.close()


def clear_database():
    # Connect to the SQLite database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Query to get a list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Iterate over the list of tables and drop each one
    for table in tables:
        table_name = table[0]
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        print(f"Dropped table: {table_name}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# clear_database()
view_table('NameTable')
