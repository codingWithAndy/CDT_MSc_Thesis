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
                round_number       = get_round_num(session['user'])
                percent = int(round((round_number / 92) * 100, 0))
                print(percent)
                total_combinations = get_total_combinations(session['user'])
                if round_number != total_combinations:
                    combo_id       = get_combinations(round_number,session['user'])
                    tweet1_content = get_tweet_content(combo_id['tweet_1'])
                    tweet2_content = get_tweet_content(combo_id['tweet_2']) 
                    tweet1, tweet2, tweet1_id, tweet2_id = tweet1_content, tweet2_content, combo_id['tweet_1'], combo_id['tweet_2']
                else:
                    msg = "You have complaed all the comparisons, please provide feedback on your experience."
                    flash(msg, 'info')
                    return redirect(url_for('feedback'))
            else:
                return redirect(url_for('signup'))
        except:
            return redirect(url_for('logout'))
            
    
    if request.method == 'POST':
        radio_1       = request.form.get('radio')
        justification = request.form.get('content')

        if radio_1 == None:
            message = "You have missed some required information. Please try again"
            flash(message, "info")
            return redirect(url_for('compare'))
        else:
            round_number = get_round_num(session['user'])
            percent = round_number / 92
            update_result(round_number,radio_1,session['user'])
            record_justification(round_number,session['user'],justification)
            update_round_number(session['user'])

            return redirect(url_for('compare'))
            
    return render_template('compare.html', tweet1 = tweet1, tweet2 = tweet2, 
                            tweet1_id = tweet1_id, tweet2_id = tweet2_id, 
                            percent = int(percent)) 


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
                return render_template('login.html')
        except:
            msg = "An issue happened. Please try again."
            flash("You have been signed up successfully.", "info")
            return redirect('index')

    if request.method == 'POST':
        try:
            email    = request.form.get('email')
            password = request.form.get('password')
            user     = login_user(email,password)
            
            if user == None:
                msg = "This email address or password mightbe wrong, please try again. Additionally, You might need to sign up instead."
                flash(msg, 'info')
                return redirect(url_for('login'))
            else:
                session['user']  = user
                session['email'] = email
                flash("You have been logged in successfully.", "info")
                return redirect(url_for('index'))
        except:
            flash("Email address does not exist, please sign up.", "info")
            return redirect(url_for('signup'))


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
            session['email'] = email

            if success == True:
                flash("You have been signed up successfully.", "info")
                return redirect(url_for('index'))
            else:
                flash("Email address already exists, please try logging in instead.", "info")
                return redirect(url_for('signup'))
        else:
            flash("Invalid email and/or passwords do not match.", "info")
            return redirect(url_for('signup'))


@app.route('/reset_password/', methods=['GET','POST'])
def reset_password():
    if request.method == 'GET':
        return render_template('forgotten_password.html')
    
    if request.method == 'POST':
        auth  = init_auth()
        email = request.form.get('email')

        print(email)
        auth.send_password_reset_email(email)

        return redirect(url_for('login'))


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