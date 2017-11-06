from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User model."""

    __tablename__ = 'users'

    # FIXME: change user_id to attorney number?
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mailing_address = db.Column(db.String(100), nullable=False)
    # FIXME: what is syntax for default value?
    firm_name = db.Column(db.String(64), default='ABC Firm', nullable=False)

    def __repr__(self):
        """Provide info about the user instance."""

        return "<Name fname={} lname={}>".format(self.fname, self.lname)

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
    settled = db.Column()




# FIXME: everything below this needs to be updated

##############################################################################
# Helper functions

def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///animals'
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