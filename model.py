from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# FIXME: add relationships to users? with secondary?


class User(db.Model):
    """User model."""

    __tablename__ = 'users'

    # FIXME: change user_id to attorney number (natural primary key)
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


class Team(db.model):
    """Team model.

    An association of users to cases so that multiple users may work on a case."""

    __tablename__ = 'teams'

    team_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    case_no = db.Column(db.Integer, db.ForeignKey('cases.case_no'), nullable=False)
    # FIXME: where should this boolean live???
    team_lead = db.Column(db.Boolean, default=True, nullable=True)


class Case(db.Model):
    """Case model."""

    __tablename__ = 'cases'

    # FIXME: change to natural primary key: case number assinged (from OCR)
    case_no = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    opposing_id = db.Column(db.Integer, db.ForeignKey('opposing_counsel.opposing_id'), nullable=False)
    plaintiff_id = db.Column(db.Integer, db.ForeignKey('plaintiffs.plaintiff_id'), nullable=False)
    claim_type_id = db.Column(db.Integer, db.ForeignKey('claim_type.claim_type_id'), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    court_name = db.Column(db.String(25), nullable=False)
    county = db.Column(db.String(25), nullable=False)
    # add court_dept and/or judge_name?
    initialized = db.Column(db.DateTime, nullable=False)
    # FIXME: should I make a settlement amount association table? with case id, settlement id, and settlement amount
    settlement_amount = db.Column(db.Integer, nullable=True)
    settled = db.Column(db.Boolean, default=False, nullable=False)

    # <FIXME -- go through team as secondary? do I need to order by?> Define relationship to user
    user = db.relationship('User', backref=db.backref('cases', order_by=case_no))

    def __repr__(self):
        """Provide info about the case instance."""

        return "<Case case_no={} initialized={}>".format(self.case_no,
                                                         self.initialized)


class OpposingCounsel(db.Model):
    """Opposition model."""

    __tablename__ = 'opposing_counsel'

    opposing_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    mailing_address = db.Column(db.String(100), nullable=False)
    firm_name = db.Column(db.String(64), nullable=False)

    # Define relationship to a case
    case = db.relationship('Case', backref=db.backref('opposing_counsel'))

    def __repr__(self):
        """Provide info about the opposing counsel instance."""

        return "<Name fname={} lname={}, from firm_name={}>".format(self.fname,
                                                                    self.lname,
                                                                    self.firm_name)

# FIXME: consolidate plaintiff and client as a 'parties' table? with an Enum column 
# w/ defendant, plaintiff, party to defendant, party to plaintiff

class Plaintiff(db.model):
    """Plaintiff model."""

    __tablename__ = 'plaintiffs'

    plaintiff_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(25), nullable=True)
    lname = db.Column(db.String(25), nullable=True)
    company = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    mailing_address = db.Column(db.String(100), nullable=False)
    # FIXME: country? town? state? 'location'?
    resident_of = db.Column(db.String(64), nullable=False)

    # Define relationship to a case
    case = db.relationship('Case', backref=db.backref('plaintiffs'))

    def __repr__(self):
        """Provide info about the plaintiff instance."""

        # FIXME: use NLP to know if person or entity
        if fname and lname:
            return "<Name fname={} lname={}>".format(self.fname, self.lname)
        elif company:
            return "<Company company={}>".format(self.company)


class Client(db.model):
    """Client model."""

    __tablename__ = 'clients'

    client_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(25), nullable=True)
    lname = db.Column(db.String(25), nullable=True)
    company = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    mailing_address = db.Column(db.String(100), nullable=False)
    # FIXME: country? town? state? 'location'?
    resident_of = db.Column(db.String(64), nullable=False)

    # Define relationship to a case
    case = db.relationship('Case', backref=db.backref('clients'))

    def __repr__(self):
        """Provide info about the client instance."""

        # FIXME: use NLP to know if person or entity
        if fname and lname:
            return "<Name fname={} lname={}>".format(self.fname, self.lname)
        elif company:
            return "<Company company={}>".format(self.company)


class DocType(db.model):
    """Doctype model."""

    __tablename__ = 'doc_types'

    doc_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide into about the document type."""

        return "<Document name={}>".format(self.name)


class ClaimType(db.model):
    """Claim type model."""

    __tablename__ = 'claim_types'

    claim_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide into about the claim type."""

        return "<Claim name={}>".format(self.name)


class Complaint(db.model):
    """Complaint (document type) model."""

    __tablename__ = 'complaints'

    complaint_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    doc_type_id = db.Column(db.Integer, db.ForeignKey('doc_types.doc_type_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    case_no = db.Column(db.Integer, db.ForeignKey('cases.case_no'), nullable=False)
    date_received = db.Column(db.DateTime, nullable=False)
    date_reviewed = db.Column(db.DateTime, nullable=True)
    date_submitted = db.Column(db.DateTime, nullable=True)
    # should this be a Date column type?
    date_filed = db.Column(db.String(25), nullable=True)
    incident_date = db.Column(db.String(25), nullable=False)
    incident_location = db.Column(db.String(100), nullable=False)
    incident_description = db.Column(db.Text, nullable=False)
    damages_asked = db.Column(db.String(100), nullable=False)
    # syntax for a file path?
    pdf = db.Column
    txt_file = db.Column

    # Define relationship to a case
    case = db.relationship('Case', backref=db.backref('complaint'))

    def __repr__(self):
        """Provide into about the complaint instance."""

        return "<Complaint complaint_id={} case_no={}>".format(self.complaint_id,
                                                               self.case_no)


class Answer(db.model):
    """Answer (document type) model."""

    __tablename__ = 'answers'

    answer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    #do I need to include complaint_id???
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.complaint_id'), nullable=False)
    doc_type_id = db.Column(db.Integer, db.ForeignKey('doc_types.doc_type_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    case_no = db.Column(db.Integer, db.ForeignKey('cases.case_no'), nullable=False)
    date_received = db.Column(db.DateTime, nullable=False)
    date_reviewed = db.Column(db.DateTime, nullable=True)
    date_submitted = db.Column(db.DateTime, nullable=True)
    #should this be seprate from date_submitted when it's from our end???
    date_filed = db.Column(db.String(25), nullable=True)
    # syntax for a file path?
    pdf = db.Column
    txt_file = db.Column

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


def connect_to_db(app, db_uri='postgres:///legalease'):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///legalease'
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