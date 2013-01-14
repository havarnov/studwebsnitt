# -*- coding: utf-8 -*-
from __future__ import division

import os

from flask import Flask
from flask import render_template, request, flash, url_for, redirect, session

from wtforms import Form, TextAreaField, PasswordField, validators

from settings import SECRET

# dictionary to translate grade to number grade
GRADE_DICT = {
        'a': 5,
        'b': 4,
        'c': 3,
        'd': 2,
        'e': 1,
        }

# dictinary to translate number grade to grade
NUMBER_DICT= {
        5: 'a',
        4: 'b',
        3: 'c',
        2: 'd',
        1: 'e',
        }

# function to determine if an str can be casted to an float.
def is_float(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

class Subject(object):
    """Class for holding info about an subject.

    """
    
    def __init__(self, date, code, name, grade, points):
        self.date = date
        self.code = code
        self.name = name
        self.grade = grade
        self.points = points

    def __eq__(self, other):
        return self.date == other.date and\
               self.code == other.code and\
               self.name == other.name and\
               self.grade == other.grade and\
               self.points == other.points

    def tuplify(self):
        """
        Returns a tuple of all the member variables.
        """
        return (
                self.date,
                self.code,
                self.name,
                self.grade,
                self.points,
            )

def extract_subjects(karakter_data):
    """
    This function takes a large string as input. It will split it by 
    linebreakes and tabs. The data is expected to be on the form after
    it's splitted by linebreakes:

    "Vår 2010   TTK4105     Reguleringsteknikk  Skriftlig   Skriftlig   28.05.2010  10128   B   7,5"

    or

    "Vår 2012   TDT4102     Prosedyre- og objektorientert programmering Skriftlig   Skriftlig   19.05.2012  10574   A   7,5 [statistikk]    07-jun-2012"

    For each line it will make a Subject object with the extracted data.
    And then return a list of all the Subject objects.

    :param karakter_data: a large str with karaterdata. CopyPasted as-is from 
    studweb.
    :type karater_data: str.
    :returns: a list of Subject objects made from the extracted data.
    :raises:

    """
    # the list that will contain all the subjects
    subjects = []

    # split the input data by linebreaks and iterate through all of them
    for line in karakter_data.split('\n'):
        # split the line by tabs
        line_splitted = line.split('\t')

        # check if line_splitted contains enough info
        # if not: throw away the data.
        if len(line_splitted) >= 9:
            # extract the different data from line_splitted
            date = line_splitted[0]
            code = line_splitted[1].replace(" ", "")
            name = line_splitted[2]
            grade = line_splitted[7]
            # the points need a "." decimal delimiter, not ","
            points_str = line_splitted[8].replace(',','.')

            # check if this data really is karakter data.
            # if not: throw away the data.
            if len(grade) == 1 and grade.isalpha() and is_float(points_str):
                # cast points_str to a float.
                points = float(points_str)

                # make the new Subject object.
                new_subject = Subject(date, code, name, grade, points)

                # append the new object to the subjects list.
                subjects.append(new_subject)

    # return the list of subjects
    return subjects

def calculate_snitt(subjects):
    """
    Calculate the "snitt" from a list of Subject objects.

    :param subjects: a list of Subject objects.
    :type subjects: list.
    :returns: a tuple with the "snitt" in number and letter. False if not
    objects to calculate "snitt" from.

    """
    # the sum of grades and points
    sum_grades = 0
    sum_points = 0

    # iterate over all the Subject objects
    for subject in subjects:
        # add the grades and points
        sum_grades += GRADE_DICT[subject.grade.lower()]*subject.points
        sum_points += subject.points

    # try to calculate the number "snitt", return False if sum_points == 0
    try:
        snitt = sum_grades/sum_points
    except ZeroDivisionError:
        return False

    # round the "snitt" off to two decimal points
    tall_snitt = round(snitt, 2)

    # get the grade on letter form from NUMBER_DICT
    bokstav_snitt = NUMBER_DICT[round(snitt)].upper()

    # return both the "snittz"
    return (tall_snitt, bokstav_snitt)

class StudwebCopyForm(Form):
    """
    A class for making forms. Inherits from wtforms.Form.

    """
    copy = TextAreaField("CopyPaste fra Studweb", [validators.Required()])

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
    form = StudwebCopyForm(request.form)
    if request.method == "POST" and form.validate():
        subjects = extract_subjects(form.copy.data)

        snitt = calculate_snitt(subjects)
        
        if not snitt:
            flash(u"Ingen fag å regne ut snitt fra")
            return render_template("index.html", form = form)

        return render_template("result.html", snitt = snitt[0], bokstav_snitt = snitt[1], subjects = subjects)
    
    return render_template("index.html", form = form)

if __name__ == "__main__":
    app.secret_key = SECRET
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
