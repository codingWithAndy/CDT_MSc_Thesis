import sqlite3 as sql
from os import path

ROOT = path.dirname(path.relpath((__file__)))

def get_tweets():
    print("Do something")
    #with open('round', 'r') as f:
    #    lines = [line for line in f.readlines()] # f.readlines()

    lines = read_textfile()
    stripped_line = [s.rstrip() for s in lines]
    print(stripped_line)

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

    return 1, 2


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