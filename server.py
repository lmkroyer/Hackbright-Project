"""HACKBRIGHT PROJECT !!!!!!"""

import textract, requests, os, sys

from ocr import OCR_file, OCR_ppm, allowed_file, es_index_complaint
# from boxes import convert_to_image, draw_rectangles

import os

from requests_oauthlib import OAuth2Session
from github import Github
from textblob import TextBlob
from datetime import datetime
from jinja2 import StrictUndefined
from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session, url_for, send_from_directory)
from flask_debugtoolbar import DebugToolbarExtension

from model import (User, CaseUser, Case, OpposingCounsel, Role, CaseParty,
                   Party, DocType, ClaimType, Complaint, Answer, Interrogatories,
                   RequestProDocs, FundClient, connect_to_db, db)

from flask_sqlalchemy import SQLAlchemy

from werkzeug.utils import secure_filename

from docx import Document

from lit_form_classes import Answer
from corp_form_classes import LPA

from elasticsearch import Elasticsearch
from elasticsearch.client.ingest import IngestClient
from elasticsearch_dsl import Search


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
# For OAuth application
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
AUTHORIZATION_BASE_URL = 'https://github.com/login/oauth/authorize'
TOKEN_URL = 'https://github.com/login/oauth/access_token'

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app.jinja_env.undefined = StrictUndefined

UPLOAD_FOLDER = 'filestorage/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
INDEX = 'documents'


@app.route('/test_boxes')
def test_boxes():

    pass


@app.route('/welcome')
def make_lit_dashboard():
    """Render the litigation dashboard."""

    current_user = session.get('current_user')

    user_object = User.query.get(current_user)

    # Query for all cases where settled == False
    active_cases = Case.query.filter(User.user_id == current_user, Case.settled == False)
    # Count those cases
    case_count = active_cases.count()
    # Return a list of all active cases
    active_case_lst = Case.query.filter(User.user_id == current_user, Case.settled == False).all()

    return render_template('/welcome.html', active_case_lst=active_case_lst,
                                            case_count=case_count)


@app.route('/')
def index():
    """Homepage."""

    return render_template('homepage.html')


@app.route('/about_us')
def show_co_info():
    """Display information about the company."""

    return render_template('about_us.html')


@app.route('/active_cases.json')
def active_case_info():
    """JSON information about county, state for active cases. For map markers."""

    cases = {
        case.case_id: {
            'caseCounty': case.county
            # 'caseState': case.state,
            # 'caseID': case.case_id
        }
    for case in Case.query.filter(Case.settled == False).all()}

    return jsonify(cases)


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

    del session['oauth_token']
    del session['current_user']
    del session['current_user_name']

    flash('Successfully signed out')

    return redirect('/')


# TODO:
# @app.route('/register')
# def register_user():
#     """Allows user to create new account."""

#     return render_template('user_registration.html')


# TODO:
@app.route('/edit_profile')
def edit_profile():
    """Allows user to edit exisitng account details."""

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

    current_user = github_user['login']
    user_object = User.query.get(current_user)
    user_name = user_object.fname
    # switch back to this so the object is in the session, can call for id or name other places
    session['current_user'] = current_user
    session['current_user_name'] = user_name

    return redirect('/')


@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token."""

    github = OAuth2Session(client_id, token=session['oauth_token'])
    github_user = github.get('https://api.github.com/user').json()


@app.route('/dashboard_lit')
def display_lit_dashboard():
    """Display the litigation dashboard."""

    current_user = session.get('current_user')

    user_object = User.query.get(current_user)
    # Query for all cases where settled == False
    active_cases = Case.query.filter(User.user_id == current_user, Case.settled == False)

    case_count = active_cases.count()
    active_case_lst = Case.query.filter(User.user_id == current_user, Case.settled == False).all()

    return render_template('dashboard_lit.html', case_count=case_count,
                                                 active_case_lst=active_case_lst)


@app.route('/userProgress.json')
def user_progress_data():
    """Return some (fake) information about the user's yearly progress."""

    data_dict = {
        "labels": ["January", "February", "March", "April", "May", "June", "July",
                   "August", "September", "October", "November", "December"],
        "datasets": [
            {
                "label": "Cases",
                "fill": True,
                "lineTension": 0.5,
                "backgroundColor": "rgba(220,220,220,0.2)",
                "borderColor": "rgba(220,220,220,1)",
                "borderCapStyle": 'butt',
                "borderDash": [],
                "borderDashOffset": 0.0,
                "borderJoinStyle": 'miter',
                "pointBorderColor": "rgba(220,220,220,1)",
                "pointBackgroundColor": "#fff",
                "pointBorderWidth": 1,
                "pointHoverRadius": 5,
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": "rgba(220,220,220,1)",
                "pointHoverBorderWidth": 2,
                "pointRadius": 3,
                "pointHitRadius": 10,
                "data": [65, 59, 80, 81, 56, 55, 40, 48, 54, 39, 45, 62],
                "spanGaps": False},
            {
                "label": "Value",
                "fill": True,
                "lineTension": 0.5,
                "backgroundColor": "rgba(151,187,205,0.2)",
                "borderColor": "rgba(151,187,205,1)",
                "borderCapStyle": 'butt',
                "borderDash": [],
                "borderDashOffset": 0.0,
                "borderJoinStyle": 'miter',
                "pointBorderColor": "rgba(151,187,205,1)",
                "pointBackgroundColor": "#fff",
                "pointBorderWidth": 1,
                "pointHoverRadius": 5,
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": "rgba(151,187,205,1)",
                "pointHoverBorderWidth": 2,
                "pointHitRadius": 10,
                "data": [20, 22, 15, 14, 21, 21, 19, 18, 22, 20, 20, 21],
                "spanGaps": False}
        ]
    }
    return jsonify(data_dict)


@app.route('/attorneys')
def display_attorneys():
    """Display all attorneys and their availability."""

    # this can be the same as the case init -- just query for all attorneys and pass into template
    attorneys = User.query.all()

    return render_template('attorneys.html', attorneys=attorneys)


@app.route('/attorney_data.json')
def get_attny_data():
    """JSON information about attorneys and their number of active cases."""

    caseload = {}

    for user in User.query.all():
        # Return a list of that user's cases (all)
        cases = user.cases
        case_count = 0
        for case in cases:
            if case.settled == False:
                case_count += 1
        fname = user.fname
        lname = user.lname
        name = fname + ' ' + lname
        caseload[name] = case_count

    users = []
    caseVolume = []
    startColor = []
    hoverColor = []

    for attny in caseload.items():
        users.append(attny[0])
        caseVolume.append(attny[1])
        startColor.append("#00ff00")
        hoverColor.append("ff0000")

    data_dict = {
                "labels": users,
                "datasets": [
                    {   "label": ["Attorney Capacity"],
                        "data": caseVolume,
                        "backgroundColor": startColor,
                        "hoverBackgroundColor": hoverColor
                    }]
            }

    return jsonify(data_dict)


@app.route('/dashboard_corp')
def display_corp_dashboard():
    """Display the corporate dashboard."""

    funds = FundClient.query.all()

    summary_reports = FundClient.query.filter(FundClient.sum_rep == True).all()

    return render_template('dashboard_corp.html', funds=funds,
                                                  summary_reports=summary_reports)


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

    # Create a case
    new_case = Case()

    db.session.add(new_case)
    db.session.commit()

    # Create the team
    new_CaseUser1 = CaseUser(user_id=team_lead, case_id=new_case.case_id)
    new_CaseUser2 = CaseUser(user_id=attorney_1, case_id=new_case.case_id)
    new_CaseUser3 = CaseUser(user_id=attorney_2, case_id=new_case.case_id)

    db.session.add(new_CaseUser1)
    db.session.add(new_CaseUser2)
    db.session.add(new_CaseUser3)

    db.session.commit()

    new_case.team_lead = team_lead
    new_case.initialized = datetime.utcnow()
    db.session.commit()

    return render_template('/upload_complaint.html', new_case=new_case.case_id)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Lets user upload a ltigation file."""

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
        # Grab all claim types from db to pass into dropdown menu
        claims = ClaimType.query.all()
        # # Figure out of OCR'd claim type is in the db
        # selected_claim = ClaimType.query.filter(ClaimType.name == parsed_text.claim).first()

        # if selected_claim:
        #     selected_claim_name = selected_claim.name
        # # FIXME: COME BACK TO THIS!!
        # else:
        #     selected_claim_name = xyz

        print parsed_text.word_list
        print parsed_text.nouns

        new_case = request.form.get('new_case')

        return render_template('display.html', parsed_text=parsed_text,
                                               filename=filename,
                                               txt_filename=txt_filename,
                                               claims=claims,
                                               new_case=new_case)
                                               # selected_claim_name=selected_claim_name)


@app.route('/upload/ppm', methods=['POST'])
def upload_ppm():
    """Lets user upload a file."""

    user = session.get('current_user')

    if 'file' not in request.files:
        flash('No file part')
        return redirect('/')

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        flash('No selected file')
        return redirect('/')

    if uploaded_file and allowed_file(uploaded_file.filename):
        filename = secure_filename(uploaded_file.filename)
        ppm_doc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(ppm_doc)

        PPM = OCR_ppm(ppm_doc)

        # txt_filename = filename.split('.')[0]
        # txt_filename = '{txt_filename}.txt'.format(txt_filename=txt_filename)

        # Add the PPM to the db
        # add_ppm_db(parsed_text, ppm_doc)

        fund = FundClient.query.filter(FundClient.fund == PPM.fund).first()

        if not fund:
            fund = FundClient(fund=PPM.fund,
                              attorney=user,
                              mgmt_fee=PPM.mgmt_fee,
                              fund_state=PPM.jurisdiction,
                              im=PPM.manager,
                              principals=PPM.principals,
                              removal=PPM.removal,
                              leverage=PPM.leverage,
                              min_commitment=PPM.min_commitment,
                              transfers=PPM.transfers,
                              ppm=ppm_doc,
                              sum_rep=True)

            db.session.add(fund)
            db.session.commit()

    return redirect('/dashboard_corp')


@app.route('/submit_complaint', methods=['POST'])
def send_to_db():
    """Sends uploaded complaint information to database."""

    # Grab doc info
    claim_type = request.form.get('claim_type')
    legal_basis = request.form.get('legal_basis')
    damages_asked = request.form.get('damages_asked')
    # Grab opposing counsel info
    counsel_fname = request.form.get('counsel_fname')
    counsel_lname = request.form.get('counsel_lname')
    counsel_firm = request.form.get('counsel_firm')
    # Grab court info
    county = request.form.get('court_county')
    state = request.form.get('court_state')
    case_no = request.form.get('case_no')
    # Grab plaintiff info
    plaintiff_fname = request.form.get('plaintiff_fname')
    plaintiff_lname = request.form.get('plaintiff_lname')
    # Grab defendant info
    defendant_fname = request.form.get('defendant_fname')
    defendant_lname = request.form.get('defendant_lname')
    defendant_residence = request.form.get('defendant_residence')

    filename = request.form.get('filename')
    txt_filename = request.form.get('txt_filename')
    claim_type_id = request.form.get('claim_type')
    doc_type_id = 1

    # grab the case id
    case_id = request.form.get('new_case')
    case = Case.query.get(case_id)

    case.case_no = int(case_no)
    case.claim_type_id = claim_type_id
    case.damages_asked = damages_asked
    case.county = county
    case.state = state

    # Check to see whether the plaintiff exsists in the db
    plaintiff = Party.query.filter(Party.fname == plaintiff_fname,
                                      Party.lname == plaintiff_lname).first()

    if not plaintiff:
        plaintiff = Party(fname=plaintiff_fname,
                           lname=plaintiff_lname)
        db.session.add(plaintiff)
        db.session.commit()
        # new_plaintiff = Plaintiff(case=case)
        # new_plaintiff.parties.append(new_party1)
    case.parties.append(plaintiff)
    case.set_party_role(plaintiff, 'plaintiff')

    # Check to see whether the defendant exists in the db
    defendant = Party.query.filter(Party.fname == defendant_fname,
                                      Party.lname == defendant_lname).first()
    if not defendant:
        defendant = Party(fname=defendant_fname,
                           lname=defendant_lname,
                           residence=defendant_residence)
        db.session.add(defendant)
        db.session.commit()
        # new_defendant = Defendant(case=case)
        # new_defendant.parties.append()
    case.parties.append(defendant)
    case.set_party_role(defendant, 'defendant')

    # Check to see whether the opposing counsel already exists in db
    opp = OpposingCounsel.query.filter(OpposingCounsel.fname == counsel_fname,
                                             OpposingCounsel.lname == counsel_lname).first()

    # If opposing counsel already in db, add their id to the case
    if opp:
        case.opposing_id = opp
    # If not, create the opposing counsel object
    else:
        opp = OpposingCounsel(fname=counsel_fname,
                                  lname=counsel_lname,
                                  firm_name=counsel_firm)
        db.session.add(opp)
        db.session.commit()

    case.opposing_id = opp.opposing_id

    date_processed = datetime.utcnow()

    new_complaint = Complaint(doc_type_id=doc_type_id,
                              case_id=case_id,
                              date_received=case.initialized,
                              date_processed=date_processed,
                              damages_asked=damages_asked,
                              legal_basis=legal_basis,
                              doc=os.path.join(app.config['UPLOAD_FOLDER'],
                                               filename),
                              txt=os.path.join(app.config['UPLOAD_FOLDER'],
                                               txt_filename))

    db.session.add(new_complaint)
    db.session.commit()

    # Add the complaint to elasticsearch index
    es_index_complaint(new_complaint.txt, new_complaint.complaint_id, case_id, new_complaint.doc)

    session['active_case'] = case_id

    return render_template('complaint_submitted.html')

# FIXME: pass in the case_id here!!!
@app.route('/answer_init/')
def display_answer_options():
    """Display answer options to user."""

    return render_template('edit_answer.html')


@app.route('/process_answer', methods=['POST'])
def generate_answer():
    """Create an answer object from the user's selections."""

    # Return a list of the defenses a user checked
    defenses = request.form.getlist('affirmative_defenses')

    if 'active_case' in session:
        case_id = session['active_case']

        case = Case.query.get(case_id)
        complaint = case.complaint
        user = User.query.filter(User.user_id == case.team_lead).first()

        # Create and Answer and generate the document
        answer = Answer(complaint, user, defenses)
        filename = answer.insert_information()

        # Store the Answer info in the database
        answer.date_created = datetime.utcnow()
        answer.docx = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        db.session.add(answer)
        db.session.commit()

    return redirect(url_for('download', filename=filename))

# @WIP:
@app.route('/process_LPA', methods=['POST'])
def generate_lpa():
    """Create an LPA object from the user's input."""

    fund = request.form.get('fund')
    fund_state = request.form.get('fund_state')
    fund_ppp = request.form.get('fund_ppp')
    gp = request.form.get('gp')
    gp_state = request.form.get('gp_state')
    gp_address = request.form.get('gp_address')
    gp_email = request.form.get('gp_email')
    gp_sig_party = request.form.get('gp_sig_party')
    im = request.form.get('im')
    im_state = request.form.get('im_state')
    im_address = request.form.get('im_address')
    im_email = request.form.get('im_email')
    sig_date = request.form.get('sig_date')

    user = session.get('current_user')

    new_fund_client = FundClient(attorney=user,
                                 fund=fund,
                                 fund_state=fund_state,
                                 fund_ppp=fund_ppp,
                                 gp=gp,
                                 gp_state=gp_state,
                                 gp_address=gp_address,
                                 gp_email=gp_email,
                                 gp_sig_party=gp_sig_party,
                                 im=im,
                                 im_state=im_state,
                                 im_address=im_address,
                                 im_email=im_email,
                                 sig_date_lpa=sig_date)

    lpa = LPA(fund, fund_state, fund_ppp,
              gp, gp_state, gp_address, gp_email, gp_sig_party,
              im, im_state, im_address, im_email,
              sig_date)

    filename = lpa.insert_information()

    new_fund_client.lpa = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    db.session.add(new_fund_client)
    db.session.commit()

    return redirect(url_for('generated_doc', filename=filename))

# TODO: display and allow to edit before build
@app.route('/display_answer')
def display_answer():
    """Show the user the word doc to approve or edit."""

    pass


@app.route('/download/<filename>')
def generated_doc(filename):
    """Allow user access to a document via to the browser."""

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route('/d3_play')
def test_d3():

    return render_template('attorney_status.html')


@app.route('/casehistory.json')
def get_case_histories():
    """JSON information about each case history."""

    casehistory = {}

    current_user = session.get('current_user')

    user_object = User.query.get(current_user)

    # Get a list of current user's active cases
    active_case_lst = Case.query.filter(User.user_id == current_user, Case.settled == False).all()

    for case in active_case_lst:

        # If the case has a complaint, display info about it
        if case.complaint:
            complaint = case.complaint.legal_basis + ' claim' + case.complaint.damages_asked + 'damages claimed'
        else:
            complaint = 'Incomplete'

        # If the case has an answer, display info about it
        if case.answer:
            answer = 'Submitted ' + case.answer.date_submitted
        else:
            answer = 'Incomplete'

        # If the case has an interrogatory, display info about it
        if case.interrogatories:
            interrogatories = 'Submitted ' + case.interrogatories.date_submitted
        else:
            interrogatories = 'Incomplete'

        # If the case has an answer, display info about it
        if case.request_pro_docs:
            request_pro_docs = 'Submitted ' + case.request_pro_docs.date_submitted
        else:
            request_pro_docs = 'Incomplete'

            casehistory[case.case_id] = {
                                         'complaint':complaint,
                                         'answer':answer,
                                         'interrogatories':interrogatories,
                                         'request_pro_docs':request_pro_docs
                                         }

    return jsonify(casehistory)


@app.route('/summaryreport/<clientID>')
def get_summary_report(clientID):
    """Returns JSON information to populate each summary report."""

    summaryreport = {}

    fund = FundClient.query.get(clientID)

    name = fund.fund

    name_caps = name.upper()

    summaryreport[fund] = {
                           'name_caps': name_caps,
                           'name': name,
                           'jurisdiction': fund.fund_state,
                           'manager': fund.im,
                           'principals': fund.principals,
                           'min_commit': fund.min_commitment,
                           'mgmt_fee': fund.mgmt_fee,
                           'leverage': fund.leverage,
                           'reinvest': fund.reinvestment,
                           'removal': fund.removal,
                           'transfers': fund.transfers
    }

    return jsonify(summaryreport)


@app.route('/search_results/<search>')
def return_search_results(search):
    """Inputs user's search query. Outputs a list of relevant documents."""

    # search_results = {
    #                     'doc_id': {
    #                                 'path': 'abc',
    #                                 'highlights': ['text1', 'text2]'
    #                             }
    #                 }

    search_results = {}

    es.indices.refresh(index=INDEX)

    # res = es.search(index=INDEX, body={"query": {"match": {"text": search}}})

    res = es.search(index=INDEX, body={
                                        "query": {
                                            "match": {
                                                "text": search
                                                }
                                            },
                                        "highlight": {
                                            "pre_tags": ["<b>"],
                                            "post_tags": ["</b>"],
                                            "fields": {
                                                "text": {}
                                            }
                                        }
                                    })


    # s = Search.from_dict(res)

    # highlights = s.highlight(search, fragment_size=50)

    print "Got %d Hits:" % res['hits']['total']

    for hit in res['hits']['hits']:

        doc_id = "%(doc_id)s" % hit["_source"]
        search_results[doc_id] = {}

        full_path = "%(path)s" % hit["_source"]
        path = full_path.split('/')[1]


        search_results[doc_id]['path'] = path

        highlights = []

        for highlight in hit['highlight']['text']:
            highlights.append(highlight)

        # this gives a string of returned match if 1
        # matched_text = res['hits']['hits'][0]['highlight']['text'][0]

        # if more than one result, here is a list of strings of highlights:
        # res['hits']['hits'][0]['highlight']['text']

        search_results[doc_id]['highlights'] = highlights

        # search_results.append("%(path)s" % hit["_source"])
        # search_results["%(doc_id)s" % hit["_source"]] = "%(path)s" % hit["_source"]
        # search_results["%(doc_id)s" % hit["_source"]] = {'path': "%(path)s" % hit["_source",
        #                                                  'highlights': "%(highlight)s" % hit["_source"]}
    # import pdb; pdb.set_trace()

    # Return a list of paths to relevant documents
    return jsonify(search_results)


# @app.route('/')

@app.route('/ocr_by_layout')
def draw_bounding_boxes():
    """Messing around with bounding boxes and opencv library."""

    return render_template('draw_boxes.html')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)



    app.run(port=5000, host='0.0.0.0')