import sqlite3 as sql
from os import path

import pyrebase

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

def tweets_judged(comparison_id):
    """Collects the required tweet IDs from the table by the ordered comparison ID.

    Args:
        comparison_id (Int): The required ID for the tweets being compared.

    Returns:
        results (??): The records content for the supplied comparison ID.
    """
    pass


###### Firebase Connections

def connect_to_firebase():
    firebase_config = {
        "apiKey": "AIzaSyAjlnmPp71zTRrXhJ7kun_pzCXnZvLRt3A",
        "authDomain": "cj-app-e65ce.firebaseapp.com",
        "databaseURL": "https://cj-app-e65ce-default-rtdb.europe-west1.firebasedatabase.app/",
        "projectId": "cj-app-e65ce",
        "storageBucket": "cj-app-e65ce.appspot.com",
        "messagingSenderId": "407532536815",
        "appId": "1:407532536815:web:38c8c3ea2726122e0fac1a",
        "measurementId": "G-PTKRNCZJGB"
    }

    firebase = pyrebase.initialize_app(firebase_config)

    return firebase

def init_db():
    firebase = connect_to_firebase()
    firebase_db = firebase.database()

    return firebase_db

def init_auth():
    firebase = connect_to_firebase()
    firebase_auth = firebase.auth()

    return firebase_auth

def init_storage():
    firebase = connect_to_firebase()
    firebase_storage = firebase.storage()

    return firebase_storage