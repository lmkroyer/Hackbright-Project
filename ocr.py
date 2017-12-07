"""HELPER FUNCTIONS FOR SERVER"""

from textblob import TextBlob
import textract, os
from lit_form_classes import ComplaintForm
from corp_form_classes import PPMForm
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
    text = textract.process(document, method='tesseract')
    # Decode string to handle stray bytes
    decoded_text = text.decode('utf-8')

    # Instantiate ComplaintForm object
    parsed_text = ComplaintForm(decoded_text)

    # Create txt file in filestorage
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
    text = textract.process(document, method='tesseract')
    # Decode string to handle stray bytes
    decoded_text = text.decode('utf-8')

    # Instantiate PPMForm object
    parsed_text = PPMForm(decoded_text)

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
        'path': filepath,
        # 'timestamp': datetime.now(),
    }

    # Add the full text to the es index as a complaint
    es.index(index=INDEX, doc_type='complaint', id=complaint_id, body=doc)
