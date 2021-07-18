import sqlite3 as sql
from os import path

import pandas as pd
import numpy as np

ROOT = path.dirname(path.relpath((__file__)))

def get_tweets():
    print("Do something")
    #with open('round', 'r') as f:
    #    lines = [line for line in f.readlines()] # f.readlines()

    lines = read_textfile()
    stripped_line = [s.rstrip() for s in lines]
    print("1st stripped line:", stripped_line)

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

    print("strippedline2:", stripped_line[-1])
    value2 = int(stripped_line[-1]) - 1
    print("value 2:", value2)

    first_tweet, second_tweet = get_comparing_tweets_id(combinations, value2)

    print(first_tweet, second_tweet)

    first_tweet_text = get__tweet_text(first_tweet, tweets)
    second_tweet_text = get__tweet_text(second_tweet, tweets)

    return first_tweet_text, second_tweet_text


def get__tweet_text(id, all_tweet):
    tweet_text = all_tweet['tweet_text'].loc[all_tweet['tweet_id']==np.int64(id)]
    tweet_text = tweet_text.iloc[0]
    print("tweet_text:", tweet_text)
    print("tweet_text[0:]:", tweet_text[0:])
    
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

    return 2, 3

def update_results(tweet_1,  comment): #tweet_2,
    if tweet_1 != None:
        pass
        #record_result(tweet_1, tweet_2, comment)
    else:
        pass
        #record_result(tweet_2, tweet_1, comment)
    pass



# Adding Tweets to Database from CSV idea
# https://medevel.com/flask-tutorial-upload-csv-file-and-insert-rows-into-the-database/