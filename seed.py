"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
import datetime as dt
from model import ClaimType, DocType, User
from model import connect_to_db, db
from server import app


def load_claim_type():
    """Add the types of claims we can process."""

    personal_injury = ClaimType(claim_type_id=1,
                                name='Personal Injury')
    breach_of_contract = ClaimType(claim_type_id=2,
                                   name='Breach of Contract')
    divorce = ClaimType(claim_type_id=3,
                        name='Divorce')
    property_dispute = ClaimType(claim_type_id=4,
                                 name='Property Dispute')
    landlord_tenant = ClaimType(claim_type_id=5,
                                name='Landlord Tenant')
    other = ClaimType(claim_type_id=6,
                      name='Other')

    db.session.add(personal_injury, 
                   breach_of_contract,
                   divorce,
                   property_dispute,
                   landlord_tenant,
                   other)

    db.session.commit()


def load_doc_types():
    """Add the types of docs we can output."""

    complaint = DocType(doc_type_id=1,
                        name='Complaint')
    answer = DocType(doc_type_id=2,
                     name='Answer')


def load_fake_users():
    """Add user data."""

    user1 = User()

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()