import textract

def pdf_to_OCR(file_path):
    """Takes in a PDF and outputs an OCR'd txt file."""

    # with open(file_path) as ocr_text:

    text = textract.process(file_path)

    f = open('hello.txt', 'w')
    f.write(text)
    f.close()



pdf_to_OCR('test.pdf')
