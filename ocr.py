"""HELPER FUNCTIONS FOR SERVER"""

from textblob import TextBlob
import textract, os
from lit_form_classes import Complaint
from corp_form_classes import PPM
import fileinput

from elasticsearch import Elasticsearch
from elasticsearch.client.ingest import IngestClient

import json
from datetime import datetime

es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'serializer': 'JSONSerializerPython2()'}])

INDEX = 'documents'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'doc'])


def OCR_file(document):
    """Takes in a file and outputs (saves) an OCR'd txt file.

    FIXME: FORK TEXTRACT TO ACCEPT A FILE OBJECT, TO AVOID TRIPS TO SERVER."""

    # Use multi page functionality with tesseract
    #FIXME: make sure this method works with other file formats, it at least works with pdf -- may need to if / else for other file formats
    text = textract.process(document, method='tesseract')
    # Decode string to handle stray bytes
    decoded_text = text.decode('utf-8')

    # # Add the OCR'd text to elasticsearch
    # es_index_complaint(decoded_text)

    # TODO: need some logic here to check what kind of form was uploaded (add dropdown for user)
    parsed_text = Complaint(decoded_text)

    # Create txt file in filestorage -- DO I WANT TO DO THIS?
    doc_name = document.split('.')[0]
    text_path = os.path.join('{doc_name}.txt'.format(doc_name=doc_name))

    # Open a txt file or create one
    with open(text_path, 'w+') as text_file:
        # Write spellchecked text to the new file (FIXME: SHOULD THIS BE DECODED TEXT?)
        text_file.write(text)

    # Close the file
    text_file.close()

    # Return a class instance
    return parsed_text


def OCR_ppm(document):
    """Takes in a file and outputs (saves) an OCR'd txt file."""

    # Use multi page functionality with tesseract
    #FIXME: make sure this method works with other file formats, it at least works with pdf -- may need to if / else for other file formats
    text = textract.process(document, method='tesseract')
    # Decode string to handle stray bytes
    decoded_text = text.decode('utf-8')

    # # Add the OCR'd text to elasticsearch
    # es_index_complaint(decoded_text)

    # TODO: need some logic here to check what kind of form was uploaded (add dropdown for user)
    parsed_text = PPM(decoded_text)

    # print parsed_text.word_list
    # print parsed_text.sentence_list
    # print parsed_text.nouns

    # import pdb; pdb.set_trace()

    # Create txt file in filestorage -- DO I WANT TO DO THIS?
    doc_name = document.split('.')[0]
    text_path = os.path.join('{doc_name}.txt'.format(doc_name=doc_name))

    # Open a txt file or create one
    with open(text_path, 'w+') as text_file:
        # Write spellchecked text to the new file (FIXME: SHOULD THIS BE DECODED TEXT?)
        text_file.write(text)

    # Close the file
    text_file.close()

    # Return a class instance
    return parsed_text


def allowed_file(filename):
    """Checks whether an uploaded file is one of the allowed formats."""

    # Returns a boolean 'true' if allowed format
    return ('.' in filename and
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS)


# def add_ppm_db(PPM, ppm_doc):
#     """Takes in a PPM object and stores it in the database."""

#     # Check to see whether the fund exsists in the db
#     fund = FundClient.query.filter(FundClient.fund == PPM.fund).first()

#     if not fund:
#         fund = FundClient(fund=PPM.fund,
#                           mgmt_fee=PPM.mgmt_fee,
#                           fund_state=PPM.jurisdiction,
#                           im=PPM.manager,
#                           principals=PPM.principals,
#                           removal=PPM.removal,
#                           leverage=PPM.leverage,
#                           min_commitment=PPM.min_commitment,
#                           transfers=PPM.transfers,
#                           ppm=ppm_doc,
#                           sum_rep=True)

#         db.session.add(fund)
#         db.session.commit()


def es_index_complaint(text_path, complaint_id, case_id, filepath):
    """Add a document to elasticsearch index."""

    # Read in the .txt complaint passed in
    text = open(text_path, 'r').read()

    decoded_text = text.decode('utf-8')

    # For now, add only full text search; add other key values for more structured searches
    doc = {
        'case': case_id,
        'doc_id': complaint_id,
        'text': decoded_text,
        'path': filepath
        # 'timestamp': datetime.now(),
    }

    # Add the full text to the es index as a complaint
    es.index(index=INDEX, doc_type='complaint', id=complaint_id, body=doc)



    # res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
    # print(res['created'])

    # res = es.get(index="test-index", doc_type='tweet', id=1)
    # print(res['_source'])


# def generate_initial_answer(ABC):
#     """Takes in case-specific info and inserts into txt file answer template.

#     Converts txt to docx filetype. Returns docx."""

#     # Open a the answer template as a txt file
#     # with open('/forms/answer_template.txt', 'w') as answer:
#     #     # Get a string from the txt file
#     #     answer_string = answer.read()
#     #     # Decode string to handle stray bytes
#     #     decoded_text = text.decode('utf-8')
#     #     new_answer = TextBlob

#     # # Close the file
#     # text_file.close()

#     template = open('/forms/answer_template.txt', 'r')
#     template_string = template.read()
#     template.close()

#     answer = template_string.replace()

# def generate_final_answer(defenses):
#     """Takes in a list of selected defenses and a docx file and adds appropriate
#     paragraphs.

#     Outputs a final answer document."""

#     # make a dictionary with affirm defense and paragraph text
#     # start with txt file, replace small items
#     # convert to docx
#     # open docx and add the relevant paragraphs
#     # save

#     # for defense in defenses:
#     pass

# def generate_answer(defenses):

#     answer = Answer()
    # call all the methods on the answer


#text class --> pass in the text
# attributes on the text class for sentece list and word list
# call methods on attributes to extract data
#get data from text object function

#pass object into jinja
# class inherits from textblob to call textblob methods
# call the super and add extra stuff in __init__


    # TODO: 2.0 Spellcheck and render misspelled words in red font
    # TODO: 3.0 Spellcheck the OCR'd text and autofix the word
    # words = text.split(' ')
    # result_words = []

    # for word in words:
    #     c = correction(word)
    #     result_words.append(c)

    # result = ' '.join(result_words)







