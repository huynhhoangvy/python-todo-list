import os
import fire
import sqlite3
from datetime import datetime

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

conn = sqlite3.connect(DEFAULT_PATH)
cur  = conn.cursor()

sql = """
    CREATE TABLE IF NOT EXISTS todos(
        id INTEGER PRIMARY KEY,
        todos_text TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT "Incomplete",
        due_date TEXT NOT NULL,
        project_id INTEGER DEFAULT NULL
    )
"""
cur.execute(sql)

sql = """
    CREATE TABLE IF NOT EXISTS projects(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
"""
cur.execute(sql)
conn.commit()


def add_todo(todo_text):
    print("adding todo now!")
    print(todo_text)
    sql = """
        INSERT INTO todos (todos_text, due_date) VALUES (?, ?)
    """
    cur.execute(sql, (todo_text, datetime.now()))
    conn.commit()

def add_project(name):
    print("adding project now!")
    print(name)
    sql = """
        INSERT INTO projects (name) VALUES (?)
    """
    cur.execute(sql, (name,))
    conn.commit()

def list(col, type):
    if col == "due_date":
        sql = """
        SELECT * FROM todos ORDER BY due_date {}
        """.format(type)
        cur.execute(sql)
    elif col == "completed" or col == "incomplete":
        sql = """
        SELECT * FROM todos WHERE Status LIKE (?) ORDER BY due_date {}
        """.format(type)
        cur.execute(sql, (col,))
        print("fired")
    elif col == "project_id":
        sql = """
        SELECT * FROM todos  WHERE project_id = (?)
        """
        cur.execute(sql, (type,))

    conn.commit()
    results = cur.fetchall()
    for row in results:
        print(row)

def mark_complete(id):
    sql = """
        UPDATE todos SET Status = "Completed" WHERE ID = ?
    """
    print("mark completed")
    cur.execute(sql, (id,))
    conn.commit()

if __name__ == '__main__':
    fire.Fire({
        'add_todo': add_todo,
        'list': list,
        'mark_complete': mark_complete,
        'add_project': add_project,
    })
    conn.close()