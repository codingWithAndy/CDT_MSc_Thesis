import sqlite3 as sql
from os import path, remove

from flask import sessions

import pandas as pd
import numpy as np

from models import *
import pyrebase

ROOT = path.dirname(path.relpath((__file__)))

def get_tweets():
    print("Do something")
    #with open('round', 'r') as f:
    #    lines = [line for line in f.readlines()] # f.readlines()

    lines = read_textfile()
    stripped_line = [s.rstrip() for s in lines]
    #print("1st stripped line:", stripped_line)

    if len(stripped_line) > 0:
        value = int(stripped_line[-1]) + 1
        with open('round', 'a') as f:
            f.write(str(value)+"\n")
    else:
        with open('round', 'a') as f:
            f.write("1"+"\n")
    
    #judged_tweets = tweets_judged(int(stripped_line[-1]))

    #user = User.query.filter_by(username=username).first_or_404()

    # query database for the records matching value
    #con = sql.connect(path.join(ROOT, 'database.db'))
    #cur = con.cursor()
    #cur.execute('select * from comparisons where id = 1') # needs to change
    #comparisons = cur.fetchall()
    
    lines = read_textfile()
    stripped_line = [s.rstrip() for s in lines]
    # Pull in tweets from CSV
    tweets = pd.read_csv('tweetsv2.csv')
    # Pull in combinations
    combinations = pd.read_csv('tweet_vs.csv')

    #print("strippedline2:", stripped_line[-1])
    value2 = int(stripped_line[-1]) - 1
    #print("value 2:", value2)

    first_tweet, second_tweet = get_comparing_tweets_id(combinations, value2)

    #print(first_tweet, second_tweet)

    first_tweet_text = get_tweet_text(first_tweet, tweets)
    second_tweet_text = get_tweet_text(second_tweet, tweets)

    return first_tweet_text, second_tweet_text, first_tweet, second_tweet


def get_tweet_text(id, all_tweet):
    tweet_text = all_tweet['tweet_text'].loc[all_tweet['tweet_id']==np.int64(id)]
    tweet_text = tweet_text.iloc[0]
    #print("tweet_text:", tweet_text)
    #print("tweet_text[0:]:", tweet_text[0:])
    
    return tweet_text

def get_comparing_tweets_id(tweets_df, location):
    tweets_compared = tweets_df.loc[[(location)]]
    tweet1 = tweets_compared.iloc[0]['tweet_1']
    tweet2 = tweets_compared.iloc[0]['tweet_2']
    
    return np.int64(tweet1), np.int64(tweet2)


def read_textfile():
    with open('round', 'r') as f:
        lines = [line for line in f.readlines()]

    return lines     

def reload_previous_tweets():
    lines = read_textfile()
    stripped_line = [s.rstrip() for s in lines]
    value2 = int(stripped_line[-1]) - 1

    # Needs refactoring
    tweets = pd.read_csv('tweetsv2.csv')
    combinations = pd.read_csv('tweet_vs.csv')
    first_tweet, second_tweet = get_comparing_tweets_id(combinations, value2)

    first_tweet_text = get_tweet_text(first_tweet, tweets)
    second_tweet_text = get_tweet_text(second_tweet, tweets)

    return first_tweet_text, second_tweet_text, first_tweet, second_tweet

def update_results(winning_tweet_id,  comment): #tweet_2,
    lines = read_textfile()
    stripped_line = [s.rstrip() for s in lines]
    value2 = int(stripped_line[-1]) - 1

    user_id = 1 # Needs to be automated.

    combinations = pd.read_csv('tweet_vs.csv')
    results_df = pd.read_csv('results.csv')
    first_tweet, second_tweet = get_comparing_tweets_id(combinations, value2)

    winning_tweet = winning_tweet_id

    print("winning tweet type:", type(winning_tweet))

    if int(winning_tweet) == int(first_tweet):
        losing_tweet = second_tweet
    elif int(winning_tweet) == int(second_tweet):
        losing_tweet = first_tweet

    justification = comment

    results_df = results_df.append({
        "user_id": user_id,
        "tweet_1": first_tweet,
        "tweet_2": second_tweet,
        "winner_id": winning_tweet,
        "loser_id": losing_tweet,
        "comment": justification
    }, ignore_index=True)

    results_df.to_csv("results.csv", index=False)


    #if tweet_1 != None:
    #    pass
        #record_result(tweet_1, tweet_2, comment)
    #else:
    #    pass
        #record_result(tweet_2, tweet_1, comment)
    #pass



# Adding Tweets to Database from CSV idea
# https://medevel.com/flask-tutorial-upload-csv-file-and-insert-rows-into-the-database/

def create_feedback(user_name,email,feedback, user_rating, session):
    txt_contents = "User Name: " + user_name + "\n" + \
                   "Email address: " + email + "\n" + \
                   "Feedback: " + feedback + "\n" + \
                   "User Rating: " + user_rating

    with open('feedback.txt', 'w') as f:
        f.write(txt_contents)

    #Put to Cloud storage
    store_feedback_cloud('feedback.txt', session)

    #delete txt file
    if path.exists("feedback.txt"):
        remove("feedback.txt")
    else:
        print("The file does not exist")

def store_feedback_cloud(textfile_name, session):
    storage        = init_storage()
    filename       = textfile_name
    cloud_filename = "feedback/user_"+str(session["user"])

    storage.child(cloud_filename).put(filename)

def store_user_docs(textfile_name, session):
    storage        = init_storage()

    # TODO: Put user tweet txt and user tweet count txt into storage
    filename       = textfile_name
    cloud_filename = "feedback/user_"+str(session["user"])

    storage.child(cloud_filename).put(filename)

def get_user_storage_docs():
    storage        = init_storage()

    stored_doc = storage.child("doc name.txt").download("","server name.txt") ## is the variable needed?

    return stored_doc

def login_user(id, password):
    auth = init_auth()

    try:
        user = auth.sign_in_with_email_and_password(id,password)
        token = user['localId'] #['idToken']
        print("Success")

        return token
    except:
        print("invalid user or password. Please try again")

def signup_user(id,password):
    auth = init_auth()

    try:
        user = auth.create_user_with_email_and_password(id,password)
        print("Success")
        return user['localId']
    except:
        print("invalid user or password. Please try again")
    