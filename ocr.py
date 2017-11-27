"""HELPER FUNCTIONS FOR SERVER"""

from textblob import TextBlob
import textract, os
from lit_form_classes import Complaint
import fileinput

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


def generate_initial_answer(ABC):
    """Takes in case-specific info and inserts into txt file answer template.

    Converts txt to docx filetype. Returns docx."""

    # Open a the answer template as a txt file
    # with open('/forms/answer_template.txt', 'w') as answer:
    #     # Get a string from the txt file
    #     answer_string = answer.read()
    #     # Decode string to handle stray bytes
    #     decoded_text = text.decode('utf-8')
    #     new_answer = TextBlob

    # # Close the file
    # text_file.close()

    template = open('/forms/answer_template.txt', 'r')
    template_string = template.read()
    template.close()

    answer = template_string.replace()

def generate_final_answer(defenses):
    """Takes in a list of selected defenses and a docx file and adds appropriate
    paragraphs.

    Outputs a final answer document."""

    # make a dictionary with affirm defense and paragraph text
    # start with txt file, replace small items
    # convert to docx
    # open docx and add the relevant paragraphs
    # save

    # for defense in defenses:
    pass

def generate_answer(defenses):

    answer = Answer()
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







