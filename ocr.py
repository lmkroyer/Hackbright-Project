"""HELPER FUNCTIONS FOR SERVER"""

from textblob import TextBlob
import textract, os
from classes import Complaint

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'doc'])


def OCR_file(document):
    """Takes in a file and outputs (saves) an OCR'd txt file.

    FIXME: FORK TEXTRACT TO ACCEPT A FILE OBJECT, TO AVOID TRIPS TO SERVER."""

    # Use multi page functionality with tesseract
    #FIXME: make sure this method works with other file formats, it at least works with pdf -- may need to if / else for other file formats
    text = textract.process(document, method='tesseract')
    # Decode string to handle stray bytes
    decoded_text = text.decode('utf-8')

    # FIXME: need some logic here to check what kind of form was uploaded (add dropdown for user)
    parsed_text = Complaint(decoded_text)

    #import text class and instantiate text object and return it for server side, which gets passed to jinja

    # Create txt file in filestorage -- DO I WANT TO DO THIS?
    doc_name = document.split('.')[0]
    text_path = os.path.join('{doc_name}.txt'.format(doc_name=doc_name))

    # Open a txt file or create one
    with open(text_path, 'w+') as text_file:
        # Write spellchecked text to the new file (FIXME: SHOULD THIS BE DECODED TEXT?)
        text_file.write(text)

    # Close the file
    text_file.close()

    #return a class instance
    return parsed_text


def allowed_file(filename):
    return ('.' in filename and
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS)


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