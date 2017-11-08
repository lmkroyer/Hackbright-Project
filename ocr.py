"""HELPER FUNCTIONS TO OCR AND PARSE FILE"""

from textblob import TextBlob
import textract, os

def OCR_file(document):
    """Takes in a file and outputs (saves) an OCR'd txt file.

    FIXME: FORK TEXTRACT TO ACCEPT A FILE OBJECT, TO AVOID TRIPS TO SERVER."""

    # Use multi page functionality with tesseract
    #FIXME: make sure this method works with other file formats, it at least works with pdf -- may need to if / else for other file formats
    text = textract.process(document, method='tesseract')
    # Decode string to handle stray bytes
    decoded_text = text.decode('utf-8')

    # print text.find('Plaintiff ')
    # print text.find('DISTRICT COURT OF ')
    # print text.find('Case No.')

    parse_me = TextBlob(decoded_text)

    # This throws a UnicodeDecodeError
    # text = TextBlob(text)
    # text.correct()

    # Create txt file in filestorage
    doc_name = document.split('.')[0]
    text_path = os.path.join('{doc_name}.txt'.format(doc_name=doc_name))

    # Open a txt file or create one
    with open(text_path, 'w+') as text_file:
        # Write spellchecked text to the new file (FIXME: SHOULD THIS BE DECODED TEXT?)
        text_file.write(text)

    # Close the file
    text_file.close()

    return parse_me


def get_plaintiff_name(text):


    # with open('filestorage/%s.txt' % (file_finder)) as f:
    # for line in text_file.readlines():
    #     if 'Plaintiff ' in line:
    #         words = line.split(' ')
    #         tracker = 0
    #         for word in words:
    #             if word == 'Plaintiff':
    #                 tracker += 1
    #                 plaintiff_fname = words[tracker]
    #                 tracker += 1
    #                 plaintiff_lname = words[tracker]
    #             else:
    #                 tracker += 1

    # make this a global variable, outside function
    # word_list = parse_me.split()

    # tracker = 0

    # for word in word_list:
    #     if word == 'Plaintiff ':
    #         tracker += 1
    #         plaintiff_fname = word_list[tracker]
    #         tracker += 1
    #         plaintiff_lname = word_list[tracker]
    #     else:
    #         tracker += 1
    pass

def get_case_no(text):

    pass




    # TODO: 2.0 Spellcheck and render misspelled words in red font
    # TODO: 3.0 Spellcheck the OCR'd text and autofix the word
    # words = text.split(' ')
    # result_words = []

    # for word in words:
    #     c = correction(word)
    #     result_words.append(c)

    # result = ' '.join(result_words)