import textract

from requests_oauthlib import OAuth2Session

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session, url_for, send_from_directory)

from flask_debugtoolbar import DebugToolbarExtension

# from model import User, Rating, Movie, connect_to_db, db
from flask_sqlalchemy import SQLAlchemy

import requests

import os

from werkzeug.utils import secure_filename

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
# For OAuth application
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

UPLOAD_FOLDER = 'filestorage/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def file_to_OCR(filename):
    """Takes in a file and outputs an OCR'd txt file."""

    # with open(file_path) as ocr_text:
    #turn this into a txt file!!

    #this returns a STRING

    text = textract.process(filename)

    f = open('hello.txt', 'w')
    f.write(text)
    # f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    f.close()

    # return f

@app.route('/')
def index():
    """Homepage."""

    return render_template('homepage.html')

@app.route('/login')
def user_login():
    """Step 1. User authentication."""

    github = OAuth2Session(client_id)
    authorization_url, state = github.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token

    return redirect(url_for('.profile'))


@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    """
    github = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(github.get('https://api.github.com/user').json())


@app.route('/upload', methods=['POST'])
def upload_file():
    """Lets user upload a file."""

    if 'file' not in request.files:
        flash('No file part')
        return redirect('homepage.html')
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect('homepage.html')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file.close()
        return redirect(url_for('uploaded_file', filename=filename))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Broken --fix so outputs OCR file."""

    # filename = secure_filename(temp_file.filename)

    # result = send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # file = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r')

    #error: Attempted implicit sequence conversion but the response object is in direct passthrough mode.
    # text = jsonify(response.data)

    # # error: 'Response' object has no attribute 'text'
    # text = jsonify(response)

    #gets error: <Response streamed [200 OK]> is not JSON serializable
    # response = jsonify(response)


    # response = requests.get(response)
    # string = response.read().decode('utf-8')
    # json_obj = json.loads(string)

    # response = requests.get(response)
    # response_dict = response.json()

    # import pdb
    # pdb.set_trace()
    # with open (result, 'r'):

    result = send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    text = file_to_OCR(result)

    return send_from_directory(app.config['UPLOAD_FOLDER'], text)

    # filename = secure_filename(f.filename)
    # f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # return render_template('display.html', text=text)


    #this line below works, to download and display doc - see if it will work with txt file 
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')