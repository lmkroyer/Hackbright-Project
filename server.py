"""HACKBRIGHT PROJECT !!!!!!"""

import textract, requests, os, sys

# from spellcheck import correction

from ocr import OCR_file, allowed_file

from requests_oauthlib import OAuth2Session
from textblob import TextBlob
from jinja2 import StrictUndefined
from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session, url_for, send_from_directory)
from flask_debugtoolbar import DebugToolbarExtension

# from model import (User, Team, Case, OpposingCounsel, Plaintiff, Client, DocType,
#                    ClaimType, Complaint, Answer, connect_to_db, db)
from flask_sqlalchemy import SQLAlchemy

# import requests

# import os

# import spellcheck
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

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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

# HELP: how redirect to dashboard not homepage?
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
        return redirect('/')
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        flash('No selected file')
        return redirect('/')
    if uploaded_file and allowed_file(uploaded_file.filename):
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        parsed_text = OCR_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return render_template('display.html', parsed_text=parsed_text)


@app.route('/submit', methods=['POST'])
def send_to_db():
    """Sends uploaded information to database."""


    # return render_template('edit_answer.html')
    pass

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')