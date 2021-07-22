from flask import Flask, render_template, request, url_for
from flask_cors import CORS
from models import get_post, create_post, record_result
from logic import get_tweets, update_results, reload_previous_tweets

app = Flask(__name__)
CORS(app)

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
        tweet1, tweet2, tweet1_id, tweet2_id = get_tweets()
        #pass
    
    if request.method == 'POST':
        radio_1 = request.form.get('radio')
        #radio_2 = request.form.get('radio')
        justification = request.form.get('content')
        if radio_1 == None  or justification == "": #and radio_2 == None
            print("No option was selected.")
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
        pass
    
    if request.method == 'POST':
        name = request.form.get('name')
        post = request.form.get('post')
        create_post(name, post)
    
    #posts = get_post()

    return render_template('feedback.html')


if __name__ == '__main__':
    app.run(debug=True)