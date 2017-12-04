"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
import datetime as dt
from model import ClaimType, DocType, User, Role
from model import connect_to_db, db
from server import app


def load_claim_types():
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

    db.session.add(personal_injury)
    db.session.add(breach_of_contract)
    db.session.add(divorce)
    db.session.add(property_dispute)
    db.session.add(landlord_tenant)
    db.session.add(other)

    db.session.commit()


def load_doc_types():
    """Add the types of docs we can output."""

    complaint = DocType(doc_type_id=1,
                        name='Complaint')

    answer = DocType(doc_type_id=2,
                     name='Answer')

    interrogatories = DocType(doc_type_id=3,
                              name="Interrogatories")

    request_pro_docs = DocType(doc_type_id=4,
                               name="Request_Pro_Docs")

    db.session.add(complaint)
    db.session.add(answer)
    db.session.add(interrogatories)
    db.session.add(request_pro_docs)
    db.session.commit()


def load_role_types():
    """Add the types of parties to a case."""

    plaintiff = Role(role_name='plaintiff')

    defendant = Role(role_name='defendant')

    db.session.add(plaintiff)
    db.session.add(defendant)
    db.session.commit()


def load_users():
    """Add attorney user data."""

    user1 = User(user_id='theIntenseOne',
                 fname='Effy',
                 lname='Stonem',
                 email='estonem@lglease.com')

    user2 = User(user_id='theRudeOne',
                 fname='Tony',
                 lname='Stonem',
                 email='tstonem@lglease.com')

    user3 = User(user_id='theDancingOne',
                 fname='Maxxie',
                 lname='Oliver',
                 email='moliver@lglease.com')

    user4 = User(user_id='theLostOne',
                 fname='Cassie',
                 lname='Ainsworth',
                 email='cainsworth@lglease.com')

    user5 = User(user_id='theRebelOne',
                 fname='James',
                 lname='Cook',
                 email='jcook@lglease.com')

    user6 = User(user_id='theSensitiveOne',
                 fname='Sid',
                 lname='Jenkins',
                 email='sjenkins@lglease.com')

    user7 = User(user_id='theTragicOne',
                 fname='Chris',
                 lname='Miles',
                 email='cmiles@lglease.com')

    user8 = User(user_id='theFunnyOne',
                 fname='Naomi',
                 lname='Campbell',
                 email='ncampbell@lglease.com')

    user9 = User(user_id='theHonestOne',
                 fname='Franky',
                 lname='Fitzgerald',
                 email='ffitzgerald@lglease.com')

    user10 = User(user_id='thePopularOne',
                 fname='Mini',
                 lname='McGuinness',
                 email='mmcguinness@lglease.com')

    user11 = User(user_id='theDrivenOne',
                 fname='Jal',
                 lname='Fazer',
                 email='jfazer@lglease.com')

    user12 = User(user_id='theGothOne',
                 fname='Rich',
                 lname='Hardbeck',
                 email='rhardbeck@lglease.com')

    user13 = User(user_id='thePoshOne',
                 fname='Grace',
                 lname='Blood',
                 email='gblood@lglease.com')

    user14 = User(user_id='lmkroyer',
                  fname='Lindsay',
                  lname='Kroyer',
                  email='lkroyer@leglease.com')

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    db.session.add(user6)
    db.session.add(user7)
    db.session.add(user8)
    db.session.add(user9)
    db.session.add(user10)
    db.session.add(user11)
    db.session.add(user12)
    db.session.add(user13)
    db.session.add(user14)

    db.session.commit()


# def load_caseusers():
#     """Add some fake teams."""

#     caseUser1 = case

# def load_cases():
#     """Add some fake case data."""

#     case1 = Case(case_no=012345678,
#                  team_lead=user11,
#                  )

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    load_users()
    load_doc_types()
    load_claim_types()
    load_role_types()