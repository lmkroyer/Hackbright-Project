# coding: utf8

"""FACTORY OF CORPORATE FORM OBJECTS."""

from textblob import TextBlob
import re
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_COLOR, WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
import inflect


class LPAForm(object):

    _fund_ = _fundState_ = _fundPpp_ = None
    _gp_ = _gpState_ = _gpAddress_ = _gpEmail_ = _gpOrgType_ = _gpSigParty_ = None
    _im_ = _imState_ = _imAddress_ = _imEmail_ = _imOrgType_ = None
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
        attrs = [attr for attr in LPAForm.__dict__.keys()
                 if (not attr.startswith("__") and
                     not callable(LPAForm.__dict__[attr]))]

        # Make a list of all upper case attributes
        cap_attrs = [attr.upper() for attr in LPAForm.__dict__.keys()
                 if (not attr.startswith("__") and
                     not callable(LPAForm.__dict__[attr]))]

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


class PPMForm(TextBlob):

    def __init__(self, decoded_text):
        super(PPMForm, self).__init__(decoded_text)

        self.sentence_list = self.sentences
        self.fund = self.get_fund_name()
        self.mgmt_fee = self.get_mgmt_fee()
        self.jurisdiction = self.get_jurisdiction()
        self.manager = self.get_manager()
        self.principals = self.get_principals()
        self.removal = self.get_removal()
        self.leverage = self.get_indebtedness()
        self.min_commitment = self.get_min_commitment
        # self.parse()

        for sentence in self.sentences:
        # for i in range(len(self.sentence_list)):
        #     sentence = self.sentence_list[i]
            string = " ".join(sentence.split())

            # Check for each form attribute; if there, set as class attribute (else set 'N/A')
            self.mgmt_fee = PPMForm.get_mgmt_fee(string)

            self.jurisdiction = PPMForm.get_jurisdiction(string)

            self.manager = PPMForm.get_manager(string)

            self.principals = PPMForm.get_principals(string)

            self.removal = PPMForm.get_removal(string)

            self.leverage = PPMForm.get_indebtedness(string)

            self.min_commitment = PPMForm.get_min_commitment(string)

            self.transfers = PPMForm.get_transfers(string)

            self.reinvestment = PPMForm.get_reinvestment(string)

        result = self.sentences[0]
        string = str(result)

        fund = re.search(r'(?:(?!CONFIDENTIAL).)*', string).group()

        self.fund = fund.upper()

    # def parse(self):
    #     """Parses a PPM for attributes."""

    #     for sentence in self.sentences:
    #     # for i in range(len(self.sentence_list)):
    #     #     sentence = self.sentence_list[i]
    #         string = " ".join(sentence.split())

    #         # Check for each form attribute; if there, set as class attribute (else set 'N/A')
    #         self.mgmt_fee = self.get_mgmt_fee(string)

    #         self.jurisdiction = self.get_jurisdiction(string)

    #         self.manager = self.get_manager(string)

    #         self.principals = self.get_principals(string)

    #         self.removal = self.get_removal(string)

    #         self.leverage = self.get_indebtedness(string)

    #         self.min_commitment = self.get_min_commitment(string)

    #         self.transfers = self.get_transfers(string)

    #         self.reinvestment = self.get_reinvestment(string)

    # def get_fund_name(self):
    #     """Returns the name of the reviewing fund."""

    #     result = self.sentence_list[0]
    #     string = str(result)

    #     fund = re.search(r'(?:(?!CONFIDENTIAL).)*', string).group()

    #     self.fund = fund.upper()

        # return name.upper()

    # @staticmethod
    # def get_mgmt_fee(sentence):
    #     """Returns the management fee of the fund."""

    #     # if '“Management Fee”'.decode('utf-8') in sentence and '%' in sentence:
    #     if u'“Management Fee”' in sentence and '%' in sentence:

    #         percent = re.search(r"\d+.\d+\%", sentence).group()
    #         payable_when = re.search(r"(?<=\bwhich will be payable\s)(?:[A-Za-z]+){2}[A-Za-z]+", sentence).group()
    #         fee = percent + ', payable ' + payable_when

    #         return fee

    # @staticmethod
    # def get_jurisdiction(sentence):
    #     """Returns the jurisdiction of the fund entity."""

    #     if 'the “Fund”'.decode('utf-8') in sentence and 'organized under the laws' in sentence:

    #         return re.search(r"(?<=\borganized under the laws of\s)(\w+)", sentence).group()

    # @staticmethod
    # def get_manager(sentence):
    #     """Returns the manager of the fund ."""

    #     if 'the “Manager”'.decode('utf-8') in sentence and 'will be the manager of the Fund' in sentence:

    #         return re.search(r"^.*(?=(\,))", sentence).group()

    # @staticmethod
    # def get_principals(sentence):
    #     """Returns the principal(s) of the fund."""

    #     if 'the “Principals”'.decode('utf-8') in sentence or 'the “Principal”'.decode('utf-8') in sentence:

    #         prinicpals = []
    #         list_words = sentence.split(' ')

    #         for word in list_words:
    #             if word[0].isupper():
    #                 prinicpals.append(word)

    #         return ' '.join(list_words)

    # @staticmethod
    # def get_removal(sentence):
    #     """Returns the removal provision."""

    #     if 'the Manager may be removed' in sentence:

    #         return sentence

    # @staticmethod
    # def get_indebtedness(sentence):
    #     """Returns the fund's allowed use of leverage."""

    #     sentence = sentence.lower()

    #     if 'indebtedness' in sentence and 'the fund may' in sentence:

    #         return u' '.join(sentence).encode('utf-8').strip()

    # @staticmethod
    # def get_min_commitment(sentence):
    #     """Returns the minimum capital commitment."""

    #     if 'minimum capital commitment' in sentence:
    #         num = re.search(r"\d+.\d+", sentence).group()

    #         return '$' + num

    # @staticmethod
    # def get_reinvestment(sentence):
    #     """Returns the reinvestment provision."""

    #     if 'reinvestment' in sentence and 'subject to' in sentence:

    #         return sentence

    # @staticmethod
    # def get_transfers(sentence):
    #     """Returns the transfer permissions provision."""

    #     if 'proposed transfers' in sentence:

    #         return sentence


    def get_fund_name(self):
        """Return the name of the reviewing fund."""

        result = self.sentence_list[0]
        string = str(result)

        name = re.search(r'(?:(?!CONFIDENTIAL).)*', string).group()

        return name.upper()


    def get_mgmt_fee(sentence):
        """Return the management fee of the fund."""

        for i in range(len(self.sentence_list)):

            if self.sentence_list[i].find('“Management Fee”'.decode('utf-8')) != -1 and self.sentence_list[i].find('%') != -1:

                # Returns a sentence object
                sentence = self.sentence_list[i]
                # Get string from sentence object
                string = str(sentence)

                percent = re.search(r"\d+.\d+\%", string).group()
                payable_when = re.search(r"(?<=\bwhich will be payable\s)(?:[A-Za-z]+){2}[A-Za-z]+", string).group()
                fee = percent + ', payable ' + payable_when

                print fee
                return fee


    def get_jurisdiction(self):
        """Return the jurisdiction of the fund entity."""

        # import pdb; pdb.set_trace()

        for i in range(len(self.sentence_list)):

            if self.sentence_list[i].find('the “Fund”'.decode('utf-8')) != -1 and self.sentence_list[i].find('organized under the laws') != -1:

                sentence = self.sentence_list[i]
                string = str(sentence)
                return re.search(r"(?<=\borganized under the laws of\s)(\w+)", string).group()


    def get_manager(self):
        """Return the manager of the fund ."""

        for i in range(len(self.sentence_list)):

            if self.sentence_list[i].find('the “Manager”'.decode('utf-8')) != -1 and self.sentence_list[i].find('will be the manager of the Fund') != -1:

                sentence = self.sentence_list[i]
                string = str(sentence)
                return re.search(r"^.*(?=(\,))", string).group()


    def get_principals(self):
        """Return the principal(s) of the fund."""

        for i in range(len(self.sentence_list)):

            if self.sentence_list[i].find('the “Principals”'.decode('utf-8')) != -1 or self.sentence_list[i].find('the “Principal”'.decode('utf-8')) != -1:
                prinicpals = []
                sentence = self.sentence_list[i]
                string = str(sentence)
                # return re.search(r"(?<!\.\s)\b[A-Z][a-z]*\b", string)
                list_words = string.split(' ')
                for word in list_words:
                    if word[0].isupper():
                        prinicpals.append(word)

                return ' '.join(list_words)


    def get_confi(self):
        """Return confidentiality provision."""

        pass


    def get_removal(self):
        """Return the removal provision."""

        for i in range(len(self.sentence_list)):

            if self.sentence_list[i].find('the Manager may be removed') != -1:

                sentence = self.sentence_list[i]
                return str(sentence)


    def get_indebtedness(self):
        """Return the fund's allowed use of leverage."""

        for i in range(len(self.sentence_list)):

            sentence = self.sentence_list[i]
            sentence = sentence.lower()

            if sentence.find('indebtedness') != -1 and self.sentence_list[i].find('the fund may') != -1:

                result = self.sentence_list[i]
                return str(result)


    def get_min_commitment(self):
        """Return the minimum capital commitment."""

        for i in range(len(self.sentence_list)):

            if self.sentence_list[i].find('minimum capital commitment') != -1:
                sentence = self.sentence_list[i]
                string = str(sentence)
                num = re.search(r"\d+.\d+", string).group()
                return '$' + num


    def get_reinvestment(self):
        """Return the reinvestment provision."""

        for i in range(len(self.sentence_list)):

            if self.sentence_list[i].find('reinvestment') != -1 and self.sentence_list[i].find('subject to') != -1:
                sentence = self.sentence_list[i]
                return str(sentence)


    def get_transfers(self):
        """Return the transfer permissions provision."""

        for i in range(len(self.sentence_list)):

            if self.sentence_list[i].find('proposed transfers') != -1:
                sentence = self.sentence_list[i]
                return str(sentence)



