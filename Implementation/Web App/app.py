from flask import Flask, render_template, request, url_for, session, redirect, flash
from flask_cors import CORS
from models import * #get_post, create_post, record_result
from logic import * #get_tweets, update_results, reload_previous_tweets, create_feedback

import pyrebase

app = Flask(__name__)

CORS(app)
app.secret_key = "lets_judge"

# Home form load
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        with open("round", "w") as f:
            f.truncate(0)
    
    if request.method == 'POST':
        name = request.form.get('name')
        post = request.form.get('post')
        create_post(name, post)

    #posts = get_post()

    return render_template('index.html')




####################################################

# CJ compare form load
@app.route('/compare/', methods=['GET','POST'])
def compare():
    if request.method == 'GET':
        if "user" in session:
            tweet1, tweet2, tweet1_id, tweet2_id = get_tweets()
        else:
            
            return redirect(url_for('login'))
    
    if request.method == 'POST':
        radio_1 = request.form.get('radio')
        #radio_2 = request.form.get('radio')
        justification = request.form.get('content')
        if radio_1 == None  or justification == "": #and radio_2 == None
            print("No option was selected.")
            message = "You have missed some required information. Please try again"
            flash(message, "info")
            tweet1, tweet2, tweet1_id, tweet2_id = reload_previous_tweets()
        else:
            print("content of radio 1 is:", radio_1)
            #print("content of radio 2 is:", radio_2)
            print("content of justification is:", justification)
            update_results(radio_1,  justification) #radio_2,
            tweet1, tweet2, tweet1_id, tweet2_id = get_tweets()

    #tweets, vs = get_tweets(radio_1, radio_2, justification)

    return render_template('compare.html', tweet1 = tweet1, tweet2 = tweet2, tweet1_id = tweet1_id, tweet2_id = tweet2_id) 


####################################################





# CJ Explination form load.
@app.route('/explination/') #, methods=['GET','POST']
def explination():
    #if request.method == 'GET':
    #    pass
    
    #if request.method == 'POST':
    #    name = request.form.get('name')
    #    post = request.form.get('post')
    #    create_post(name, post)

    #posts = get_post()

    return render_template('explination.html')

# CJ Results form load.
@app.route('/results/', methods=['GET','POST'])
def results():
    if request.method == 'GET':
        pass
    
    if request.method == 'POST':
        name = request.form.get('name')
        post = request.form.get('post')
        create_post(name, post)
    
    #posts = get_post()

    return render_template('results.html')

@app.route('/feedback/', methods=['GET','POST'])
def feedback():
    if request.method == 'GET':
        print("feedback user:", session["user"])
    
    if request.method == 'POST':
        name     = request.form.get('name')
        email    = request.form.get('email')
        feedback = request.form.get('comments')
        rating   = request.form.get('experience')
        #print(name, email, feedback, rating)
        create_feedback(name, email, feedback, rating, session)

    return render_template('feedback.html')

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        if "user" in session:
            return redirect(url_for('logout'))
        else:
            return render_template('login.html')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_id = login_user(email,password)

        session['user'] = user_id

        print(user_id)
        print("session user:", session['user'])

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
            session['user'] = user_id

            if success == True:
                flash("You have been signed up successfully.", "info")
                return redirect(url_for('index'))
            else:
                flash("Email address already exists, please try logging in instead.", "info")
                return redirect(url_for('signup'))
        else:
            flash("Invalid email and/or passwords do not match.", "info")
            return redirect(url_for('signup'))
        #user_id = login_user(email,password)

        #session['user'] = user_id

        #print(user_id)
        #print("session user:", session['user'])

        #print(email, password)

        
@app.route('/logout/')
def logout():
    if "user" in session:
        user = session["user"]
        message = "You have been logged out succesfully"
        flash(message, "info")

    session.pop("user", None)

    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)