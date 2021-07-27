from flask import Flask, render_template, request, url_for, session, redirect, flash
from flask_cors import CORS
from models import *
from logic import * 

import pyrebase
import os
import sys
import logging

app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

CORS(app)
app.secret_key = "lets_judge"

# Home form load
@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

####################################################

# CJ compare form load
@app.route('/compare/', methods=['GET','POST'])
def compare():
    if request.method == 'GET':
        try:
            if "user" in session:
                round_number   = get_round_num(session['user'])
                combo_id       = get_combinations(round_number,session['user'])
                weet1_content  = get_tweet_content(combo_id['tweet_1'])
                tweet2_content = get_tweet_content(combo_id['tweet_2']) 
                tweet1, tweet2, tweet1_id, tweet2_id = weet1_content, tweet2_content, combo_id['tweet_1'], combo_id['tweet_2']
            else:
                return redirect(url_for('signup'))
        except:
            return redirect(url_for('logout'))
    
    if request.method == 'POST':
        radio_1       = request.form.get('radio')
        justification = request.form.get('content')

        if radio_1 == None or justification == "":
            message = "You have missed some required information. Please try again"
            flash(message, "info")
            return redirect(url_for('compare'))
            #round_number   = get_round_num(session['user'])
            #combo_id       = get_combinations(round_number,session['user'])
            #weet1_content  = get_tweet_content(combo_id['tweet_1'])
            #tweet2_content = get_tweet_content(combo_id['tweet_2']) 
            #tweet1, tweet2, tweet1_id, tweet2_id = weet1_content, tweet2_content, combo_id['tweet_1'], combo_id['tweet_2']
        else:
            round_number = get_round_num(session['user'])
            #update results
            update_result(round_number,radio_1,session['user'])
            #update justification
            record_justification(round_number,session['user'],justification)
            #update cj position
            update_round_number(session['user'])

            return redirect(url_for('compare'))
            
    return render_template('compare.html', tweet1 = tweet1, tweet2 = tweet2, tweet1_id = tweet1_id, tweet2_id = tweet2_id) 


####################################################

# CJ Explination form load.
@app.route('/explination/')
def explination():
    return render_template('explination.html')


# CJ Results form load.
@app.route('/results/', methods=['GET','POST'])
def results():
    if request.method == 'GET':
        # Expand in time
        pass
    
    if request.method == 'POST':
        # Expand in time
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
        feedback = request.form.get('comments')
        rating   = request.form.get('experience')
        
        create_feedback(name, feedback, rating, session, contact)
        msg = "thank you for the feedback!"
        flash(msg, 'info')
        return redirect(url_for('index'))

    


@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        try:
            if "user" in session:
                return redirect(url_for('logout'))
            else:
                return redirect('login')
        except:
            msg = "An issue happened. Please try again."
            flash("You have been signed up successfully.", "info")
            return redirect('index')

    
    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')
        user  = login_user(email,password)
        session['user'] = user
        session['email'] = email

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
    app.run(debug=True) #,host='0.0.0.0',port=int(os.environ.get('PORT',8080))


#auth.send_password_reset_email("email") 