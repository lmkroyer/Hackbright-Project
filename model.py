from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User model."""

    __tablename__ = 'users'

    # TODO: change user_id to natural key (attorney number) by removing autoincrement when make profile edit page
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mailing_address = db.Column(db.String(100), nullable=False)
    firm_name = db.Column(db.String(64),
                          default='Wayne, Prince & Jones LLP',
                          nullable=False)

    def __repr__(self):
        """Provide info about the user instance."""

        return "<Name fname={} lname={}>".format(self.fname, self.lname)


class CaseUser(db.Model):
    """CaseUser model.

    An association of users to cases so that multiple users may work on a case."""

    __tablename__ = 'teams'

    team_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    case_no = db.Column(db.Integer, db.ForeignKey('cases.case_no'), nullable=False)

    def __repr__(self):
        """Provide info about the CaseUser instance."""

        return "<CaseUser team_id={} user_id={} case_no={}>".format(self.team_id,
                                                                    self.user_id,
                                                                    self.case_no)


class Case(db.Model):
    """Case model."""

    __tablename__ = 'cases'

    # Natural primary key: case number assinged (from OCR)
    case_no = db.Column(db.Integer, primary_key=True)
    team_lead = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    # client_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'), nullable=False)
    # opposing_id = db.Column(db.Integer, db.ForeignKey('opposing_counsel.opposing_id'), nullable=False)
    claim_type_id = db.Column(db.Integer, db.ForeignKey('claim_types.claim_type_id'), nullable=False)
    damages_asked = db.Column(db.Integer, nullable=False)
    #below: see what is on form
    state = db.Column(db.String(25), nullable=False)
    county = db.Column(db.String(25), nullable=False)
    # add court_dept and/or judge_name?
    initialized = db.Column(db.DateTime, nullable=False)
    # FIXME: should I make a settlement amount association table? with case id, settlement id, and settlement amount
    settlement_amount = db.Column(db.Integer, nullable=True)
    settled = db.Column(db.Boolean, default=False, nullable=False)

    # Define relationship to user
    user = db.relationship('User', secondary='Team', backref=db.backref('cases'))

    def __repr__(self):
        """Provide info about the case instance."""

        return "<Case case_no={} initialized={}>".format(self.case_no,
                                                         self.initialized)


class Plaintiff(db.Model):  # or name this CaseParty?
    """Plaintiff (CaseParty) model.

    An association of parties to cases to assign plaintiff(s) to case.

    Allows parties to be both plaintiffs and defendants for different cases."""

    __tablename__ = 'plaintiffs'

    plaintiff_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'), nullable=False)
    case_no = db.Column(db.Integer, db.ForeignKey('cases.case_no'), nullable=False)

    def __repr__(self):
        """Provide info about the CaseParty instance."""

        return "<CaseParty plaintiff_id={} party_id={} case_no={}>".format(
                                                                    self.plaintiff_id,
                                                                    self.party_id,
                                                                    self.case_no)


class Defendant(db.Model):  # or name this CaseParty?
    """Defendant (CaseParty) model.

    An association of parties to cases to assign defendant(s) to case.

    Allows parties to be both plaintiffs and defendants for different cases."""

    __tablename__ = 'defendants'

    defendant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'), nullable=False)
    case_no = db.Column(db.Integer, db.ForeignKey('cases.case_no'), nullable=False)

    def __repr__(self):
        """Provide info about the Defendant instance."""

        return "<CaseParty defendant_id={} party_id={} case_no={}>".format(
                                                                    self.defendant_id,
                                                                    self.party_id,
                                                                    self.case_no)

class Party(db.Model):
    """Party model."""

    __tablename__ = 'parties'

    party_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(25), nullable=True)
    lname = db.Column(db.String(25), nullable=True)
    company = db.Column(db.String(100), nullable=True)
    # email = db.Column(db.String(100), nullable=True)
    residence = db.Column(db.String(100), nullable=True)

    # Define relationships to a case
    cases = db.relationship('Case', secondary='plaintiffs', backref=db.backref('party'))

    cases = db.relationship('Case', secondary='defendants', backref=db.backref('party'))

    def __repr__(self):
        """Provide info about the party instance."""

        # FIXME: use NLP to know if person or entity???
        if fname and lname:
            return "<Name fname={} lname={}>".format(self.fname, self.lname)
        elif company:
            return "<Company company={}>".format(self.company)


class OpposingCounsel(db.Model):
    """Opposition model."""

    __tablename__ = 'opposing_counsel'

    opposing_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    mailing_address = db.Column(db.String(100), nullable=True)
    firm_name = db.Column(db.String(64), nullable=True)

    # Define relationship to a case
    cases = db.relationship('Case', backref=db.backref('opposing_counsel'))

    def __repr__(self):
        """Provide info about the opposing counsel instance."""

        return "<Name fname={} lname={}, from firm_name={}>".format(self.fname,
                                                                    self.lname,
                                                                    self.firm_name)


class DocType(db.Model):
    """Doctype model."""

    __tablename__ = 'doc_types'

    doc_type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide into about the document type."""

        return "<Document name={}>".format(self.name)


class ClaimType(db.Model):
    """Claim type model."""

    __tablename__ = 'claim_types'

    claim_type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide into about the claim type."""

        return "<Claim name={}>".format(self.name)


class Complaint(db.Model):
    """Complaint (document type) model."""

    __tablename__ = 'complaints'

    # Meta data on document
    complaint_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # hardcode this to the value in doctype table:
    doc_type_id = db.Column(db.Integer, db.ForeignKey('doc_types.doc_type_id'), nullable=False)
    case_no = db.Column(db.Integer, db.ForeignKey('cases.case_no'), nullable=False)
    date_received = db.Column(db.DateTime, nullable=False)
    date_reviewed = db.Column(db.DateTime, nullable=True)
    date_submitted = db.Column(db.DateTime, nullable=True)
    # Substantive data from document
    # incident_date = db.Column(db.String(25), nullable=False)
    # incident_location = db.Column(db.String(100), nullable=False)
    # incident_description = db.Column(db.Text, nullable=False)
    damages_asked = db.Column(db.String(100), nullable=False)
    legal_basis = db.Column(db.String(64), nullable=True)
    # Storage location <TODO: put on AWS and change to url>
    pdf = db.Column(db.String(64), nullable=False)  # will be url if online server or relative file /static/etc...
    txt = db.Column(db.String(64), nullable=False)

    # Define relationship to a case
    case = db.relationship('Case', backref=db.backref('complaint'))

    def __repr__(self):
        """Provide into about the complaint instance."""

        return "<Complaint complaint_id={} case_no={}>".format(self.complaint_id,
                                                               self.case_no)


class Answer(db.Model):
    """Answer (document type) model."""

    __tablename__ = 'answers'

    answer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    doc_type_id = db.Column(db.Integer, db.ForeignKey('doc_types.doc_type_id'), nullable=False)
    case_no = db.Column(db.Integer, db.ForeignKey('cases.case_no'), nullable=False)

    date_created = db.Column(db.DateTime, nullable=True)
    date_reviewed = db.Column(db.DateTime, nullable=True)
    date_submitted = db.Column(db.DateTime, nullable=True)

    pdf = db.Column(db.String(64), nullable=False)  # will be url if online server or relative file /static/etc...
    txt_file = db.Column(db.String(64), nullable=False)

    # Define relationship to a case
    case = db.relationship('Case', backref=db.backref('answer'))

    def __repr__(self):
        """Provide into about the answer instance."""

        return "<Answer answer_id={} case_no={}>".format(self.answer_id,
                                                         self.case_no)


##############################################################################
# Helper functions

def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app, db_uri='postgres:///lglease'):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///lglease'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."