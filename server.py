"""HACKBRIGHT PROJECT !!!!!!"""

import textract, requests, os, sys

from ocr import OCR_file, allowed_file

from requests_oauthlib import OAuth2Session
from github import Github
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
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
# For OAuth application
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
AUTHORIZATION_BASE_URL = 'https://github.com/login/oauth/authorize'
TOKEN_URL = 'https://github.com/login/oauth/access_token'

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
    authorization_url, state = github.authorization_url(AUTHORIZATION_BASE_URL)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state

    return redirect(authorization_url)


@app.route('/signout')
def signout():
    """Signs out user and removes from session."""

    flash('Successfully signed out')
    del session['oauth_state']

    return redirect('/')


# @app.route('/register')
# def register_user():
#     """Allows user to create new account."""

#     return render_template('user_registration.html')


@app.route('/edit_profile')
def edit_profile():
    """Allows user to edit exisitng account details."""

    # FIXME: grad the user object for user who is logged in
    # user = User.query

    return render_template('edit_profile.html')


@app.route('/confirm_new_account', methods=["POST"])
def add_user():
    """Add new user to database."""

    pass


@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to the registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. Use that to obtain an access token.
    """

    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(TOKEN_URL, client_secret=client_secret,
                               authorization_response=request.url)

    # At this point we can fetch protected resources but let's save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token

    github = OAuth2Session(client_id, token=session['oauth_token'])
    github_user = github.get('https://api.github.com/user').json()
    print github_user

    return redirect(url_for('/profile'))


# @app.route("/profile", methods=["GET"])
# def profile():
#     """Fetching a protected resource using an OAuth 2 token."""

#     github = OAuth2Session(client_id, token=session['oauth_token'])
#     github_user = github.get('https://api.github.com/user').json()
# # find user info here: https://developer.github.com/apps/building-integrations/setting-up-and-registering-github-apps/identifying-users-for-github-apps/
#     import pdb
#     pdb.set_trace()

#     return 'hello world'


@app.route('/dashboard_lit')
def display_lit_dashboard():
    """Display the litigation dashboard."""

    return render_template('dashboard_lit.html')


@app.route('/dashboard_corp')
def display_corp_dashboard():
    """Display the corporate dashboard."""

    return render_template('dashboard_corp.html')


@app.route('/case_init')
def start_case():
    """Allow user to initialize a team and case by uploading complaint."""


    attorneys = User.query.all()

    return render_template('case_init.html', attorneys=attorneys)


@app.route('/process_users', methods=['POST'])
def create_team():
    """Add the selected attorneys to a team and create a case_id."""

    # Grab user ids
    team_lead = request.form.get('team_lead')
    attorney_1 = request.form.get('attorney_1')
    attorney_2 = request.form.get('attorney_2')

    # Create a case object
    new_case = Case()
    db.session.add(case)
    db.session.commit()

    # Create the team
    new_case.team_lead = team_lead
    new_CaseUser1 = CaseUser(user=team_lead, case=new_case)
    new_CaseUser2 = CaseUser(user=attorney_1, case=new_case)
    new_CaseUser3 = CaseUser(user=attorney_2, case=new_case)

    db.session.add(new_CaseUser1, new_CaseUser2, new_CaseUser3)

    db.session.commit()

    return render_template('/upload_complaint.html', new_CaseUser1=new_CaseUser1,
                                                     new_CaseUser2=new_CaseUser2,
                                                     new_CaseUser3=new_CaseUser3,
                                                     new_case=new_case)


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

        txt_filename = filename.split('.')[0]
        txt_filename = '{txt_filename}.txt'.format(txt_filename=txt_filename)

        return render_template('display.html', parsed_text=parsed_text,
                                               filename=filename,
                                               txt_filename=txt_filename)


@app.route('/submit_complaint', methods=['POST'])
def send_to_db():
    """Sends uploaded complaint information to database."""

    # Grab doc info
    claim_type = request.form.get('claim_type')
    legal_basis = request.form.get('legal_basis')
    damages_asked = request.form.get('damages_asked')
    date_processed = request.form.get('complaint_date')
    # Grab opposing counsel info
    counsel_fname = request.form.get('counsel_fname')
    counsel_lname = request.form.get('counsel_lname')
    counsel_firm = request.form.get('counsel_firm')
    counsel_address = request.form.get('counsel_address')
    # Grab court info
    court_county = request.form.get('county')
    court_state = request.form.get('state')
    case_no = request.form.get('case_no')
    # Grab plaintiff info
    plaintiff_fname = request.form.get('plaintiff_fname')
    plaintiff_lname = request.form.get('plaintiff_lname')
    # Grab defendant info
    defendant_fname = request.form.get('defendant_fname')
    defendant_lname = request.form.get('defendant_lname')
    defendant_residence = request.form.get('defendant_residence')

    filename = request.form.get('filename')

    # Grab the case and team information we seeded earlier
    case = request.form.get('case')
    team_lead = new_CaseUser1
    attorney1 = new_CaseUser2
    attorney2 = new_CaseUser3

    # FIXME: figure out how to pass this in
    doc_type_id = 1

    # FIXME: check those entries that may already be in there!!!!!
    # FIXME: how do I handle giving it to users who are logged in??
    # FIXME: how to handle claim type / claim type id?

    # when log in with oauth, put user id in the session

    # FIXME: pass in the case id
    new_case = Case(case_no=case_no,
                    team_lead=USER,
                    claim_type_id=claim_type_id,
                    damages_asked=damages_asked,
                    county=court_county,
                    state=court_state,
                    initialized=date_processed)

    db.session.add(new_case)

    new_party1 = Party(fname=plaintiff_fname,
                       lname=plaintiff_lname)

    db.session.add(new_party1)

    new_plaintiff = Plaintiff(case=new_case,
                              party=new_party1)

    db.session.add(new_plaintiff)

    new_party2 = Party(fname=defendant_fname,
                       lname=defendant_lname,
                       residence=defendant_residence)

    db.session.add(new_party2)

    new_defendant = Defendant(case=new_case,
                              party=new_party2)

    db.session.add(new_defendant)

    new_opp = OpposingCounsel(fname=counsel_fname,
                              lname=counsel_lname,
                              mailing_address=counsel_address,
                              firm_name=counsel_firm)

    db.session.add(new_opp)

    new_case.opposing_id = new_opposing_counsel

    # if autoincrement primary key, add and commit to get to it before any next steps
    # can add pieces at a time before commit whole thing, even if missing inforation

    #new_case.[attribute] =

    new_complaint = Complaint(doc_type_id=doc_type_id,
                              case=new_case,
                              date_received=date_processed,
                              damages_asked=damages_asked,
                              legal_basis=legal_basis,
                              pdf=os.path.join(app.config['UPLOAD_FOLDER'],
                                               filename),
                              txt=os.path.join(app.config['UPLOAD_FOLDER'],
                                               txt_filename))

    db.session.add(new_complaint)
    db.session.commit()

    return render_template('complaint_submitted.html')


@app.route('/answer_init')
def display_answer_options():
    """Display answer options to user."""

    return render_template('edit_answer.html')


@app.route('/display_answer')
def display_answer():
    """Show the user the word doc to approve or edit.

    FIXME: or just generate it????"""


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')