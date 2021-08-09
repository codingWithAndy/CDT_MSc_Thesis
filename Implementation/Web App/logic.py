#import sqlite3 as sql
from logging import root
from os import path, remove
from itertools import combinations as combs
from sklearn.utils import shuffle
#import spacy
#from spacy import displacy

from flask import sessions

import pandas as pd
import numpy as np
import operator
import random

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
        #print("Log in Successful")

        #send email verification
        auth.send_email_verification(user['idToken'])  

        #combs_of_tweets   = [i for i in range(1,11)]
        #id_combination = [" , ".join(map(str, comb)) for comb in combs(combs_of_tweets, 2)]

        #combination_df = pd.DataFrame()

        #r = 1
        #for each_combination in id_combination:
        #    split = each_combination.split(' , ')
        #    combination_df = combination_df.append({
        #        "combination_id": str(r),
        #        "tweet_1": split[0],
        #        "tweet_2": split[1]
        #    }, ignore_index=True)
        #    r += 1

        #combination_df = shuffle(combination_df)

        tweet_2_id = [i for i in range(1,11)]
        #id_15_combination = [" , ".join(map(str, comb)) for comb in combs(tweet_2_id, 2)]
        id_combs = list(combs(tweet_2_id, 2))
        random.shuffle(id_combs)

        used_nums = []
        new_pairs = []

        for each_pair in id_combs:
            if each_pair[0] not in used_nums:
                if each_pair[1] not in used_nums:
                    used_nums.append(each_pair[0])
                    used_nums.append(each_pair[1])
                    new_pairs.append(each_pair)

        combs_df = pd.DataFrame()

        r = 1
        for each_combination in new_pairs:
            #split = each_combination.split(' , ')
            combs_df = combs_df.append({
                "combination_id": str(r),
                "tweet_1": str(each_combination[0]),
                "tweet_2": str(each_combination[1])
            }, ignore_index=True)

            r += 1

        combination_df = combs_df.reset_index(drop=True)

        for i in combination_df.index:
            dict_data = combination_df.loc[i].to_dict()
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

    if winner_id == combination['tweet_1']:
        loser_id = int(combination['tweet_2'])
    else:
        loser_id = int(combination['tweet_1'])

    tweets = db.child("results").child(int(winner_id)).get()
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




def calculate_score(id):
    db = init_db()
    tweets_scores = db.child("results").child(id).get()
    dict = {}
    for tweet in tweets_scores.each():
        dict[tweet.key()] = tweet.val()

    result = dict['win'] - dict['lose']

    return result

def display_ranking():
    db = init_db()
    
    order_dict = {}
    for i in range(1,11):
        tweet_details = db.child("results").child(i).get()
        dict = {}
        for tweet in tweet_details.each():
            dict[tweet.key()] = tweet.val()

        order_dict[i] = dict
    
    new_order = {}
    for i in range(1,11):
        new_order[i] = order_dict[i]['score']
    
    new_order = sorted(new_order.items(), key=lambda kv: kv[1], reverse=True)
    
    final_order = {}
    for i in range(len(new_order)):
        final_order[new_order[i][0]] = new_order[i][1]

    final_order_content = {}
    for key in final_order:
        final_order_content[key] = get_tweet_content(key)
    
    return final_order, final_order_content





def update_cj_score():
    db = init_db()
    # TODO: Don't hard code this check.
    for i in range(1,11):
        score = calculate_score(i)
        db.child("results").child(i).update({'score': score})

#def get_ner():
#    tweet = get_tweet_content(1)
#    text = tweet #"When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously."

#    nlp = spacy.load("en_core_web_sm")
#    doc = nlp(text)

#    html = displacy.render(doc, style="ent")
#    dependency = displacy.render(doc, style="dep")
#   result = html
#
#    return result, dependency
    