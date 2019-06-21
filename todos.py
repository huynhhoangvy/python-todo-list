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
        project_id INTEGER DEFAULT NULL,
        user_id INTEGER DEFAULT NULL
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

sql = """
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email_address TEXT NOT NULL
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

def add_user(name, email):
    print("adding user now!")
    print(name, email)
    sql = """
        INSERT INTO users (name, email_address) VALUES (?, ?)
    """
    cur.execute(sql, (name, email,))
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
        SELECT * FROM todos WHERE project_id = (?)
        """
        cur.execute(sql, (type,))

    conn.commit()
    results = cur.fetchall()
    for row in results:
        print(row)

def list_projects ():
    sql = """
    SELECT * FROM projects ORDER BY id
    """
    cur.execute(sql)
    conn.commit()
    results = cur.fetchall()
    for row in results:
        print(row)

def list_users ():
    sql = """
    SELECT * FROM users ORDER BY id
    """
    cur.execute(sql)
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

def staff():
    sql = """
    SELECT DISTINCT users.name, projects.name
    FROM todos
    LEFT JOIN users
    ON todos.user_id = users.id
    LEFT JOIN projects
    ON todos.project_id = projects.id
    """
    cur.execute(sql)
    conn.commit()
    results = cur.fetchall()    
    for row in results:
        print(row)

def who_to_fire():
    sql = """
    SELECT users.id, users.name, users.email_address
    FROM users
    LEFT JOIN todos
    ON todos.user_id = users.id
    WHERE todos.todos_text is NULL
    """
    cur.execute(sql)
    conn.commit()
    results = cur.fetchall()    
    for row in results:
        print(row)

if __name__ == '__main__':
    fire.Fire({
        'add_todo': add_todo,
        'list': list,
        'mark_complete': mark_complete,
        'add_project': add_project,
        'list_projects': list_projects,
        'add_user': add_user,
        'list_users': list_users,
        'staff': staff,
        'who_to_fire': who_to_fire
    })
    conn.close()