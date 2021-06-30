import sqlite3 as sql
from os import path

ROOT = path.dirname(path.relpath((__file__)))

def create_post(name, content):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()

    cur.execute('insert into posts (name, content) values (?, ?)', (name, content)) # needs to change
    con.commit()
    con.close()

def get_post():
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('select * from posts') # needs to change
    posts = cur.fetchall()

    return posts