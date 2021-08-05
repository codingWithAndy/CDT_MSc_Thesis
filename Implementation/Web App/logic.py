#import sqlite3 as sql
from os import path, remove
from itertools import combinations as combs
from sklearn.utils import shuffle

from flask import sessions

import pandas as pd
import numpy as np

from models import *
import pyrebase

ROOT = path.dirname(path.relpath((__file__)))

# Adding Tweets to Database from CSV idea
# https://medevel.com/flask-tutorial-upload-csv-file-and-insert-rows-into-the-database/

def create_feedback(name,feedback, user_rating, session, contact): #user_name,email,feedback, user_rating, session
    db = init_db()

    info = {
        'email': session['email'], 
        'name': name,
        'user_rating': user_rating,
        'feedback': feedback,
        'contact': contact,
        'user_id': session['user']
    }

    db.child("user_feedback").child(session['user']).update(info)

############################ Firebase Connections ######################################
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
    """
    Connecting the web app to the firebase authenication to return a user ID.

    Args:
        id ([str]): the users email address to be checked for auth.
        password ([str]): the users password to conform the auth.

    Returns:
        token [str]: this contains the returned local id for the auth.
    """
    auth = init_auth()

    try:
        user  = auth.sign_in_with_email_and_password(id,password)
        token = user['localId'] #['idToken']
        
        return token
    except:
        print("invalid user or password. Please try again")


def signup_user(id,password):
    auth = init_auth()
    db = init_db()

    try:
        user = auth.create_user_with_email_and_password(id,password)
        init_cj_round_number(user['localId'])
        print("Log in Successful")

        #send email verification
        auth.send_email_verification(user['idToken'])  

        combs_of_tweets   = [i for i in range(1,15)]
        id_15_combination = [" , ".join(map(str, comb)) for comb in combs(combs_of_tweets, 2)]

        combination_15_df = pd.DataFrame()

        r = 1
        for each_combination in id_15_combination:
            split = each_combination.split(' , ')
            combination_15_df = combination_15_df.append({
                "combination_id": str(r),
                "tweet_1": split[0],
                "tweet_2": split[1]
            }, ignore_index=True)
            r += 1

        combination_15_df = shuffle(combination_15_df)
        combination_15_df = combination_15_df.reset_index(drop=True)

        for i in combination_15_df.index:
            dict_data = combination_15_df.loc[i].to_dict()
            tweet_id = i+1
            db.child("combinations").child(user['localId']).child(tweet_id).set(dict_data)

        return True, user['localId']
    except:
        return False, None
    
    
def init_cj_round_number(user_id):
    db = init_db()
    db.child("cj_position").child(user_id).update({'comparison_no': 1})


########## Firebase Exploration ########
def update_round_number(user_id):
    db = init_db()
    current_round = get_round_num(user_id)

    db.child("cj_position").child(user_id).update({'comparison_no': current_round + 1})

def get_round_num(user_id):
    db = init_db()
    round_info = db.child("cj_position").child(user_id).get()
    
    for cj_position in round_info.each():
        current_num = cj_position.val()
    
    return current_num

def record_justification(round_number,user_id,justification):
    db = init_db()
    db.child("justification").child(user_id).child(round_number).update({'justification': justification})

def update_result(round_number,winner_id,user_id):
    db = init_db()
    combination = get_combinations(round_number,user_id)

    if str(winner_id) == combination['tweet_1']:
        loser_id = int(combination['tweet_2'])
    else:
        loser_id = int(combination['tweet_1'])

    tweets = db.child("results").child(winner_id).get()
    tweet_dict = {}
    for tweet in tweets.each():
        tweet_dict[tweet.key()] = tweet.val()
    tweet_dict['win'] += 1

    other_tweet = db.child("results").child(loser_id).get()
    other_tweet_dict = {}
    for tweet in other_tweet.each():
        other_tweet_dict[tweet.key()] = tweet.val()
    other_tweet_dict['lose'] += 1

    db.child("results").child(winner_id).update({"win": tweet_dict['win']})
    db.child("results").child(loser_id).update({"lose": other_tweet_dict['lose']})


def get_combinations(round_number,user_id):
    db = init_db()
    combination = db.child("combinations").child(user_id).child(round_number).get()
    combo_dict = {}
    for combo in combination.each():
        combo_dict[combo.key()] = combo.val()

    return combo_dict

def get_tweet_content(id):
    db = init_db()
    tweets = db.child("results").child(id).get()
    dict = {}
    for tweet in tweets.each():
        dict[tweet.key()] = tweet.val()

    return dict['content']

def get_total_combinations(user_id):
    db = init_db()
    rounds_no = db.child('combinations').child(user_id).get()

    count = 0
    for each_combo in rounds_no.each():
        count += 1

    return count