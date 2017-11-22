"""FACTORY OF CORPORATE FORM OBJECTS."""

from textblob import TextBlob
import re
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_COLOR, WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
import inflect


class LPA(object):

    _fund_ = _sigdate_ = defendant_fname = defendant_lname = None
    case_state = case_county = user_fname = user_lname = user_mailing_address = None
    user_email = user_firm_name = case_no = None

    def __init__(self, complaint, user):

        self.complaint = complaint
        self.user = user
        self.plaintiff_fname = complaint.case.plaintiffs[0].fname
        self.plaintiff_lname = complaint.case.plaintiffs[0].lname
        self.defendant_fname = complaint.case.defendants[0].fname
        self.defendant_lname = complaint.case.defendants[0].lname
        self.case_county = complaint.case.county
        self.case_state = complaint.case.state
        self.user_fname = user.fname
        self.user_lname = user.lname
        self.user_email = user.email
        self.user_mailing_address = user.mailing_address
        self.user_firm_name = user.firm_name
        self.case_no = str(complaint.case.case_no)


    def insert_information(self):
        """Adds custom information into the request for production of documents template.

        Returns a modified docx file."""

        # Make a list of all attributes on a RequestProDocs class
        attrs = [attr for attr in RequestProDocs.__dict__.keys()
                 if (not attr.startswith("__") and
                     not callable(RequestProDocs.__dict__[attr]))]

        # Make a list of all upper case attributes
        cap_attrs = [attr.upper() for attr in RequestProDocs.__dict__.keys()
                 if (not attr.startswith("__") and
                     not callable(RequestProDocs.__dict__[attr]))]

        # Make a Document object for Python-docx
        request_pro_docs = Document('forms/request_for_production_of_docs_template.docx')
        style = request_pro_docs.styles['Normal']
        font = style.font
        font.size = Pt(12)

        # font.highlight_color = WD_COLOR.YELLOW

        # Preserve format: replace lowercase tags with values
        for attr_name in attrs:

            for paragraph in request_pro_docs.paragraphs:

                if attr_name in paragraph.text:
                    paragraph.text = (
                        paragraph.text.replace(attr_name,
                                               getattr(self, attr_name)))

        # Preserve format: replace uppercase tags with values
        for attr_name in cap_attrs:

            for paragraph in request_pro_docs.paragraphs:

                if attr_name in paragraph.text:
                    attr_data = getattr(self, attr_name.lower())
                    attr_data = attr_data.upper()
                    paragraph.text = (
                        paragraph.text.replace(attr_name, attr_data))

        # Make a new filename from case no.
        filename = 'request_pro_docs_{case_no}.docx'.format(case_no=self.case_no)
        # Save the modified document with the new filename
        request_pro_docs.save('filestorage/{filename}'.format(filename=filename))
        # Return filename to pass to display
        return filename