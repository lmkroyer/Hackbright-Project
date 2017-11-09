"""FACTORY OF FORM OBJECTS.

Send this to the server (import there) and use in jinja."""

from textblob import TextBlob
import re


class Complaint(TextBlob):
    def __init__(self, decoded_text):
        super(Complaint, self).__init__(decoded_text)

        self.word_list = self.split()
        self.sentence_list = self.sentences
        self.plaintiff_fname = self.get_plaintiff_fname()
        self.plaintiff_lname = self.get_plaintiff_lname()
        self.case_no = self.get_case_no()
        self.county = self.get_county()
        self.defendant_fname = self.get_defendant_fname()
        self.defendant_lname = self.get_defendant_lname()
        self.defendant_residence = self.get_defendant_residence()
        self.amount_claimed = self.get_amount_claimed()
        self.claim = self.get_claim()
        self.counsel_fname = self.get_counsel_fname()
        self.counsel_lname = self.get_counsel_lname()

        # etc...

# FIXME: refactor option to consolidate double ifs in one line, and return the self. (no name)

    def get_plaintiff_fname(self):
        """Return the plaintiff's first name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'Plaintiff':
                plaintiff_fname = self.word_list[i + 1]
                return plaintiff_fname


    def get_plaintiff_lname(self):
        """Return the plaintiff's last name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'Plaintiff':
                plaintiff_lname = self.word_list[i + 2]
                return plaintiff_lname


    def get_case_no(self):
        """Return the plaintiff's last name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'Case':
                if self.word_list[i + 1] == 'No.2':
                    case_no = self.word_list[i + 2]
                    return case_no


    def get_county(self):
        """Return the county in CA."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'COUNTY':
                if self.word_list[i + 1] == 'OF':
                    county = self.word_list[i + 2]
                    return county


    def get_defendant_fname(self):
        """Return the defendant's first name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'defendant':
                defendant_fname = self.word_list[i + 1]
                return defendant_fname


    def get_defendant_lname(self):
        """Return the defendant's last name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'defendant':
                defedant_lname = self.word_list[i + 2]
                return defedant_lname


    def get_amount_claimed(self):
        """Return the dollar of damages requested."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'Amount':
                if self.word_list[i + 1] == 'claimed':
                    amount_claimed = self.word_list[i + 2]
                    return amount_claimed


    def get_claim(self):
        """Return the type of claim as either the default PI or an error message."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'Personal':
                if self.word_list[i + 1] == 'Injury':
                    claim = 'Personal Injury'
            else:
                claim = 'UNDEFINED'
            return claim


    def get_defendant_residence(self):
        """Return the defendant's city, county, state of residence."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'resides':
                defendant_residence = self.word_list[i + 2:i + 6]
                return defendant_residence


    def get_counsel_fname(self):
        """Return the opposing counsel's first name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'P.C.':
                counsel_fname = self.word_list[i + 2]
                return counsel_fname


    def get_counsel_lname(self):
        """Return the opposing counsel's last name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'P.C.':
                counsel_lname = self.word_list[i + 4]
                return counsel_lname

class Answer(TextBlob):
    pass 