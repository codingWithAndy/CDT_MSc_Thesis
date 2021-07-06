import sqlite3 as sql
from os import path

ROOT = path.dirname(path.relpath((__file__)))

def create_post(tweet_content, tweet_likes, tweet_retweets, tweet_interactions):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()

    cur.execute('insert into tweets (tweet_content, tweet_likes, tweet_retweets, tweet_interactions) values (?, ?, ?, ?)', (tweet_content, tweet_likes, tweet_retweets, tweet_interactions)) # needs to change
    con.commit()
    con.close()

def record_result(winner_id, loser_id, comment):
    with open('round', 'r') as f:
        lines = [line for line in f.readlines()] # f.readlines()

    stripped_line = [s.rstrip() for s in lines]
    
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()

    cur.execute('insert into cj_results (winner_id, loser_id, comment) values (?, ?, ?)', (winner_id, loser_id, comment)) # needs to change
    con.commit()
    con.close()

def get_post():
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('select * from posts') # needs to change
    comparisons = cur.fetchall()

    return comparisons
