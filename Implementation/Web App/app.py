from flask import Flask, render_template, request, url_for
from flask_cors import CORS
from models import get_post, create_post

#from logic import [Required function]

# Needs to change copy and paste from social media app so far.
app = Flask(__name__)

CORS(app)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        pass
    
    if request.method == 'POST':
        name = request.form.get('name')
        post = request.form.get('post')
        create_post(name, post)

    #posts = get_post()

    return render_template('index.html')

@app.route('/compare/', methods=['GET','POST'])
def compare():
    if request.method == 'GET':
        pass
    
    if request.method == 'POST':
        name = request.form.get('name')
        post = request.form.get('post')
        create_post(name, post)

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

if __name__ == '__main__':
    app.run(debug=True)