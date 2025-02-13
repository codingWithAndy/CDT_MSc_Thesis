from flask import Flask, render_template, request, url_for, session, redirect, flash
from flask_cors import CORS
from models import * #get_post, create_post, record_result
from logic import * #get_tweets, update_results, reload_previous_tweets, create_feedback

import pyrebase
import os

app = Flask(__name__)

CORS(app)
app.secret_key = "lets_judge"

# Home form load
@app.route('/', methods=['GET','POST'])
def index():
    #if request.method == 'GET':
        #with open("round", "w") as f:
        #    f.truncate(0)
    #    pass
    
    #if request.method == 'POST':
    #    name = request.form.get('name')
    #    post = request.form.get('post')
    #    create_post(name, post)

    #posts = get_post()

    return render_template('index.html')

####################################################

# CJ compare form load
@app.route('/compare/', methods=['GET','POST'])
def compare():
    if request.method == 'GET':
        if "user" in session:
            round_number = get_round_num(session['user'])
            combo_id = get_combinations(round_number)
            weet1_content = get_tweet_content(combo_id['tweet_1'])
            tweet2_content = get_tweet_content(combo_id['tweet_2']) 
            tweet1, tweet2, tweet1_id, tweet2_id = weet1_content, tweet2_content, combo_id['tweet_1'], combo_id['tweet_2']
            #tweet1, tweet2, tweet1_id, tweet2_id = get_tweets()
        else:
            return redirect(url_for('login'))
    
    if request.method == 'POST':
        radio_1       = request.form.get('radio')
        justification = request.form.get('content')
        #radio_2 = request.form.get('radio')
        if radio_1 == None or justification == "": #and radio_2 == None
            #print("No option was selected.")
            message = "You have missed some required information. Please try again"
            flash(message, "info")
            round_number = get_round_num(session['user'])
            combo_id = get_combinations(round_number)
            weet1_content = get_tweet_content(combo_id['tweet_1'])
            tweet2_content = get_tweet_content(combo_id['tweet_2']) 
            tweet1, tweet2, tweet1_id, tweet2_id = weet1_content, tweet2_content, combo_id['tweet_1'], combo_id['tweet_2']
            #tweet1, tweet2, tweet1_id, tweet2_id = reload_previous_tweets()
        else:
            round_number = get_round_num(session['user'])
            #combo_id = get_combinations(round_number)
            #update results
            update_result(round_number,radio_1)
            #update justification
            record_justification(round_number,session['user'],justification)

            #update cj position
            update_round_number(session['user'])

            return redirect(url_for('compare'))
            #print("content of radio 1 is:", radio_1)
            #print("content of justification is:", justification)
            #update_results(radio_1,  justification) #radio_2,
            #tweet1, tweet2, tweet1_id, tweet2_id = get_tweets()

    #tweets, vs = get_tweets(radio_1, radio_2, justification)

    return render_template('compare.html', tweet1 = tweet1, tweet2 = tweet2, tweet1_id = tweet1_id, tweet2_id = tweet2_id) 


####################################################

# CJ Explination form load.
@app.route('/explination/') #, methods=['GET','POST']
def explination():
    return render_template('explination.html')


# CJ Results form load.
@app.route('/results/', methods=['GET','POST'])
def results():
    if request.method == 'GET':
        pass
    
    if request.method == 'POST':
        pass
    
    return render_template('results.html')


@app.route('/feedback/', methods=['GET','POST'])
def feedback():
    if request.method == 'GET':
        if "user" in session:
            return render_template('feedback.html')
        else:
            return redirect(url_for('login'))
    
    if request.method == 'POST':
        name     = request.form.get('name')
        contact  = request.form.get('contact')
        #email    = session['email']#request.form.get('email')
        feedback = request.form.get('comments')
        rating   = request.form.get('experience')
        #print(name, email, feedback, rating)
        create_feedback(name, feedback, rating, session, contact)
        msg = "thank you for the feedback!"
        flash(msg, 'info')
        return redirect(url_for('index'))#render_template('index.html')

    


@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        if "user" in session:
            return redirect(url_for('logout'))
        else:
            return render_template('login.html')
    
    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')
        user  = login_user(email,password)
        session['user'] = user
        session['email'] = email

        print("Session email:", session['email'])
        #print("session user:", session['user'])

        flash("You have been logged in successfully.", "info")
        
        return redirect(url_for('index'))


@app.route('/signup/', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')
        password_check = request.form.get('password_check')

        if password == password_check:
            success, user_id = signup_user(email,password)
            session['user']  = user_id

            if success == True:
                flash("You have been signed up successfully.", "info")
                return redirect(url_for('index'))
            else:
                flash("Email address already exists, please try logging in instead.", "info")
                return redirect(url_for('signup'))
        else:
            flash("Invalid email and/or passwords do not match.", "info")
            return redirect(url_for('signup'))
        

@app.route('/logout/')
def logout():
    if "user" in session:
        user    = session["user"]
        message = "You have been logged out succesfully"
        flash(message, "info")

    session.pop("user", None)

    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT',8080)))


#auth.send_password_reset_email("email") 