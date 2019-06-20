import os
import sqlite3

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

conn = sqlite3.connect(DEFAULT_PATH)

sql = """
    CREATE TABLE IF NOT EXISTS todos(
        id INTERGER PRIMARY KEY,
        todos_text TEXT NOT NULL
    )
"""

cur  = conn.cursor()
cur.execute(sql)




conn.close()


