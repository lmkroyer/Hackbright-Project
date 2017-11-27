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

    _fund_ = _fdState_ = _fundPpp_ = None
    _gp_ = _gpState_ = _gpAddress_ = _gpEmail_ = _gpSigParty_ = None
    _im_ = _imState_ = _imAddress_ = _imEmail_ = None
    _sigDate_ = None

    def __init__(self, fund, fund_state, fund_ppp,
                 gp, gp_state, gp_address, gp_email, gp_sig_party,
                 im, im_state, im_address, im_email,
                 sig_date):

        self._fund_ = fund
        self._fundState_ = fund_state
        self._fundPpp_ = fund_ppp
        self._gp_ = gp
        self._gpOrgType_ = self.spell_gp_org()
        self._gpState_ = gp_state
        self._gpAddress_ = gp_address
        self._gpEmail_ = gp_email
        self._gpSigParty_ = gp_sig_party
        self._im_ = im
        self._imOrgType_ = self.spell_im_org()
        self._imState_ = im_state
        self._imAddress_ = im_address
        self._imEmail_ = im_email
        self._sigDate_ = sig_date


    def spell_gp_org(self):
        """Return the full spelling of the GP's organizational type."""

        gp = self._gp_
        gp_org = gp.split(' ')[-1]

        if gp_org == 'LP':
            return 'Limited Partnership'
        elif gp_org == 'LLC':
            return 'Limited Liability Company'


    def spell_im_org(self):
        """Return the full spelling of the IM's organizational type."""

        im = self._im_
        im_org = im.split(' ')[-1]

        if im_org == 'LP':
            return 'Limited Partnership'
        elif im_org == 'LLC':
            return 'Limited Liability Company'


    def insert_information(self):
        """Adds custom information into the request for production of documents template.

        Returns a modified docx file."""

        # Make a list of all attributes on a RequestProDocs class
        attrs = [attr for attr in LPA.__dict__.keys()
                 if (not attr.startswith("__") and
                     not callable(LPA.__dict__[attr]))]

        # Make a list of all upper case attributes
        cap_attrs = [attr.upper() for attr in LPA.__dict__.keys()
                 if (not attr.startswith("__") and
                     not callable(LPA.__dict__[attr]))]

        # Make a Document object for Python-docx
        lpa = Document('forms/lpa_template.docx')
        style = lpa.styles['Normal']
        font = style.font
        font.size = Pt(10)

        # Preserve format: replace lowercase tags with values
        for attr_name in attrs:

            for paragraph in lpa.paragraphs:

                if attr_name in paragraph.text:
                    paragraph.text = (
                        paragraph.text.replace(attr_name,
                                               getattr(self, attr_name)))

        # Preserve format: replace uppercase tags with values
        for attr_name in cap_attrs:

            for paragraph in lpa.paragraphs:

                if attr_name in paragraph.text:
                    attr_data = getattr(self, attr_name.lower())
                    attr_data = attr_data.upper()
                    paragraph.text = (
                        paragraph.text.replace(attr_name, attr_data))

        # Make a new filename from fund name
        filename = 'LPA_{fund}.docx'.format(fund=self._fund_)
        # Save the modified document with the new filename
        lpa.save('filestorage/{filename}'.format(filename=filename))
        # Return filename to pass to display
        return filename