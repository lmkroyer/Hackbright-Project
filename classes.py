"""FACTORY OF FORM OBJECTS."""

from textblob import TextBlob
import re
from datetime import datetime
from docx import Document
from defenses import all_defenses


# FIXME: remove all punctuation!!!! so don't have to do weird searches

class Complaint(TextBlob):
    def __init__(self, decoded_text):
        super(Complaint, self).__init__(decoded_text)

        self.word_list = self.words
        self.sentence_list = self.sentences
        self.plaintiff_fname = self.get_plaintiff_fname()
        self.plaintiff_lname = self.get_plaintiff_lname()
        self.case_no = self.get_case_no()
        self.county = self.get_county()
        self.state = self.get_state()
        self.defendant_fname = self.get_defendant_fname()
        self.defendant_lname = self.get_defendant_lname()
        self.defendant_residence = self.get_defendant_residence()
        self.amount_claimed = self.get_amount_claimed()
        self.claim = self.get_claim()
        self.counsel_fname = self.get_counsel_fname()
        self.counsel_lname = self.get_counsel_lname()
        self.counsel_firm = self. get_counsel_firm()
        self.complaint_date = self.get_complaint_date()
        self.legal_basis = self.get_legal_basis()
        # self.injury_date = self.get_injury_date()
        # self.injury_location = self.get_injury_location()
        # self.injury_description = self.get_injury_description()

        # etc...

# FIXME: refactor option to consolidate double ifs in one line, and return the self. (no name)
# FIXME: remove punctuation from word list so can not hardcode that into checks
# FIXME: .correct() everything that comes out
# FIXME: a way to grab other defendants and/or check if company or person

    # Could also check if what comes after starts with upper case, and if so pull it
    def get_plaintiff_fname(self):
        """Return the plaintiff's first name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'Plaintiff':
                plaintiff_fname = self.word_list[i + 1]
                return plaintiff_fname.capitalize()


    def get_plaintiff_lname(self):
        """Return the plaintiff's last name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'Plaintiff':
                plaintiff_lname = self.word_list[i + 3]
                return plaintiff_lname.capitalize()


    def get_case_no(self):
        """Return the plaintiff's last name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'Case' and self.word_list[i + 1] == 'No':
                case_no = self.word_list[i + 2]
                return case_no


    def get_county(self):
        """Return the county."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'COUNTY':
                if self.word_list[i + 1] == 'OF':
                    county = self.word_list[i + 2]
                    return county.capitalize()


    def get_state(self):
        """Return the state."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'STATE':
                if self.word_list[i + 1] == 'OF':
                    state = self.word_list[i + 2]
                    return state.capitalize()


    def get_defendant_fname(self):
        """Return the defendant's first name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'defendant':
                return self.word_list[i + 1]


    def get_defendant_lname(self):
        """Return the defendant's last name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'defendant':
                return self.word_list[i + 2]


    def get_amount_claimed(self):
        """Return the dollar of damages requested."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'Amount':
                if self.word_list[i + 1] == 'claimed':
                    return self.word_list[i + 2]


    def get_claim(self):
        """Return the type of claim as either the default PI or an error message."""

        for i in range(len(self.sentence_list)):

            if self.sentence_list[i].find('Personal Injury'):
                return 'Personal Injury'
            else:
                return 'UNKNOWN'


    def get_legal_basis(self):
        """Return the types of legal claims made in the complaint.

        TODO: (2.0) allow multiple legal bases."""

        # result = []

        for i in range(len(self.word_list)):

        #     if self.sentence_list[i].find('Negligence') and 'Negligence' not in result:
        #         result.append('Negligence')
        #     # etc.
        # result = ' '.join(result)
            if self.word_list[i] == 'Claim' and self.word_list[i + 1] == 'for' and self.word_list[i + 2] == 'Relief':
            #     if self.word_list[i + 3] not in result:
            #         result.append(self.word_list[i + 3])
            # result = ' '.join(result)
                return self.word_list[i + 3]


    def get_defendant_residence(self):
        """Return the defendant's city, county, state of residence."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'resides':
                defendant_residence = self.word_list[i + 2:i + 6]
                result = ' '.join(defendant_residence)
                return result[:-1]
                #FIXME: turn this into a geocode here?

    def get_counsel_fname(self):
        """Return the opposing counsel's first name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'P.C':
                return self.word_list[i + 2]


    def get_counsel_lname(self):
        """Return the opposing counsel's last name."""

        for i in range(len(self.word_list)):
            if self.word_list[i] == 'P.C' or self.word_list[i] == 'LLC':
                return self.word_list[i + 4]


    def get_counsel_firm(self):
        """Return the opposing counsel's firm name."""

        firm = self.sentence_list[-3]
        return firm.title()


    def get_complaint_date(self):
        """Stampe the complaint with the date processed."""

        return datetime.utcnow()


    def get_injury_date(self):

        return 'N/A'

        # regex: 'On *** plaintiff was'


    def get_injury_location(self):

        return 'N/A'


    def get_injury_description(self):

        return 'N/A'

class Answer(object):

    def __init__(self, complaint, user, defenses):

# pass a complaint into the answer, and loop through complaint attributes and set to answer
# method that takes in self and generates a document
# make info inside brackets match so can set as variable and check all brackets
# look up: get attr and set attr (takes in a variable, find attribute that matches that and set)

        self.complaint = complaint
        self.user = user
        self.defenses = defenses
        self.plaintiff_fname = complaint.case.plaintiffs.fname
        self.plaintiff_lname = complaint.case.plaintiffs.lname
        self.defendant_fname = complaint.case.defendants.fname
        self.defendant_lname = complaint.case.defendants.lname
        self.case_county = complaint.case.county
        self.case_state = complaint.case.state
        # this gets the ID for the user marked as team lead
        # self.team_lead = complaint.cases.team_lead
        # self.user = user
        self.user_fname = user.fname
        self.user_lname = user.user_lname
        self.user_email = user.user_email
        self.user_mailing_address = user.mailing_address
        self.user_firm_name = user.firm_name
        self.case_no = complaint.case_no


    def insert_information():
        """Adds custom information into the answer template.

        Returns a modified docx file."""
        # FIXME: add pronoun awareness (textblob)!!! on the extract from dictionary point.
        # Grab a value, turn to textblob object, change gender pronount, and then insert
        # FIXME: change civil code #s so that state gets input as variable

        # Make a dictionary of all attributes on an Answer class
        attrs = Answer.__dict__

        answer = Document('/forms/answer_template.docx')
        # FIXME: account for caps and lower
        for attr in attrs:

            for p in answer.paragraphs:
                if attr in p.text:
                    inline = p.runs
                    # Loop added to work with runs (strings with same style)
                    for i in range(len(inline)):
                        if attr in inline[i].text:
                            text = inline[i].text.replace(attr, attrs[attr])
                            inline[i].text = text
                    # do I need to print here?
                    print p.text
        # FIXME: make this its own method on the class
        for defense in defenses:
            # set a counter variable, to know how to label a paragraph
            # FIXME: when insert, convert this to word version of number
            # counter_letters = 1
            # counter_num = 2

            for p in answer.paragraphs:
                # if 'AFFIRMATIVE DEFENSE' in p.text:
                #     inline = p.runs
                #     # Grab the legalese from the dictionary - a string of text
                #     legalese = all_defenses[defense]

                #     # Add a paragraph
                #     # FIXME: add a number at the beginning of each paragraph
                #     # FIXME: add a tab after the starting number
                #     INSERT VAR(counter) + "AFFIRMATIVE DEFENSE"
                #     INSERT legalese
                #     # Loop added to work with runs (strings with same style)
                #     for i in range(len(inline)):
                #         if attr in inline[i].text:
                #             text = inline[i].text.replace(attr, attrs[attr])
                #             inline[i].text = text
                #     # do I need to print here?
                #     print p.text
                if 'AFFIRMATIVE DEFENSE' in p.text:
                    para = p._p
                    # Grab the legalese from the dictionary - a string of text
                    legalese = all_defenses[defense]

                    # Add a paragraph
                    # FIXME: add a number at the beginning of each paragraph
                    # FIXME: add a tab after the starting number
                    para.addnext(counter, "AFFIRMATIVE DEFENSE", '/n', legalese)

                    # do I need to print here?
                    print p.text

        answer.save('/filestorage/answer_{case_no}.docx'.format(case_no=self.case_no))
        # return something to pass to display



# don't assume end coordinate
# give user option to draw
# function returns list
# iterate over and crop box/image for each item
# draw image with text returned (opencv)
# algorithm: given this location and image, where can i place it?
# tiling project






