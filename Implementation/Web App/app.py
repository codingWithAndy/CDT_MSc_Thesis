from flask import Flask, render_template, request, url_for
from flask_cors import CORS
from models import get_post, create_post

from logic import get_tweets

# Needs to change copy and paste from social media app so far.
app = Flask(__name__)

CORS(app)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        with open("workfile", "w") as f:
            f.truncate(0)
    
    if request.method == 'POST':
        name = request.form.get('name')
        post = request.form.get('post')
        create_post(name, post)

    #posts = get_post()

    return render_template('index.html')

@app.route('/compare/', methods=['GET','POST'])
def compare():
    if request.method == 'GET':
        #tweets = get_tweets()
        pass
    
    if request.method == 'POST':
        radio_1 = request.form.get('radio 1')
        radio_2 = request.form.get('radio 2')
        print("content of radio 1 is:", radio_1)
        print("content of radio 2 is:", radio_2)
        #post = request.form.get('post')
        #create_post(name, post)
        pass

    tweets = get_tweets()
    #posts = get_post()

    return render_template('compare.html')

@app.route('/explination/', methods=['GET','POST'])
def explination():
    if request.method == 'GET':
        pass
    
    if request.method == 'POST':
        name = request.form.get('name')
        post = request.form.get('post')
        create_post(name, post)

    #posts = get_post()

    return render_template('explination.html')

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

if __name__ == '__main__':
    app.run(debug=True)