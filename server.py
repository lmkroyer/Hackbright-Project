"""HACKBRIGHT PROJECT !!!!!!"""

import textract, requests, os, sys

reload(sys)
sys.setdefaultencoding('Cp1252')

# from spellcheck import correction

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
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'doc'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return ('.' in filename and
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS)


def OCR_file(document):
    """Takes in a file and outputs (saves) an OCR'd txt file.

    FIXME: FORK TEXTRACT TO ACCEPT A FILE OBJECT, TO AVOID TRIPS TO SERVER."""

    # Use multi page functionality with tesseract
    #FIXME: make sure this method works with other file formats, it at least works with pdf -- may need to if / else for other file formats
    text = textract.process(document, method='tesseract')

    # print text.find('Plaintiff ')
    # print text.find('DISTRICT COURT OF ')
    # print text.find('Case No.')

    parse_me = TextBlob(text)

    # This throws a UnicodeDecodeError
    # text = TextBlob(text)
    # text.correct()

    # TODO: 2.0 Spellcheck and render misspelled words in red font
    # TODO: 3.0 Spellcheck the OCR'd text and autofix the word
    # words = text.split(' ')
    # result_words = []

    # for word in words:
    #     c = correction(word)
    #     result_words.append(c)

    # result = ' '.join(result_words)

    # Create txt file in filestorage
    doc_name = document.split('.')[0]
    text_path = os.path.join('{doc_name}.txt'.format(doc_name=doc_name))

    # Open a txt file or create one
    with open(text_path, 'w+') as text_file:
        # Write spellchecked text to the new file
        text_file.write(text)

    # Close the file
    text_file.close()

    return parse_me


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
        OCR_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        #now start playing with extraction
        file_finder = filename.split('.')[0]

        # OCR_file = file_finder + '.txt'

        with open('filestorage/%s.txt' % (file_finder)) as f:

            # line = f.rstrip()
            for line in f:

                if 'Plaintiff ' in line:
                    words = line.split(' ')
                    tracker = 0
                    for word in words:
                        if word == 'Plaintiff':
                            tracker += 1
                            plaintiff_fname = words[tracker]
                            tracker += 1
                            plaintiff_lname = words[tracker]
                        else:
                            tracker += 1

        # experiment with textblob

        #this returns a list of noun phrases for blob
        nouns = parse_me.noun_phrases




        #all working up to here!!!
        return render_template('display.html', plaintiff_fname=plaintiff_fname,
                                               plaintiff_lname=plaintiff_lname)

        #can we from here to ocr function?
        # uploaded_file.close()
        # return redirect(url_for('uploaded_file', filename=filename))


# Presently uncesseary below
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     """Displays uploaded file."""

#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/submit', methods=['POST'])
def send_to_db():
    """Sends uploaded information to database."""

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