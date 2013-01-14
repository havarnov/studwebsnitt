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

def listify_subjects(subjects):
    """This function will translate all the Subject objects in 
    the input variable into a tuple with all the data.

    """
    result = []
    for subject in subjects:
        result.append((
            subject.date,
            subject.code,
            subject.name,
            subject.grade,
            subject.points,))
    return result

class StudwebCopyForm(Form):
    """
    A helper class for making forms. Inherits from wtforms.Form.

    """
    copy = TextAreaField("CopyPaste fra Studweb", [validators.Required()])

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
    form = StudwebCopyForm(request.form)
    if request.method == "POST" and form.validate():
        subjects = []
        for line in form.copy.data.split('\n'):
            line_splitted = line.split('\t')
            if len(line_splitted) >= 9:
                date = line_splitted[0]
                code = line_splitted[1]
                name = line_splitted[2]
                grade = line_splitted[7]
                points_str = line_splitted[8].replace(',','.')
                if len(grade) == 1 and grade.isalpha() and is_float(points_str):
                    points = float(points_str)
                    new_subject = Subject(date, code, name, grade, points)
                    subjects.append(new_subject)

        sum_grades = 0
        sum_points = 0
        for subject in subjects:
            sum_grades += GRADE_DICT[subject.grade.lower()]*points
            sum_points += subject.points

        try:
            snitt = sum_grades/sum_points
        except ZeroDivisionError:
            flash(u"Ingen fag å regne ut snitt fra")
            return render_template("index.html", form = form)
        tall_snitt = round(snitt, 2)
        bokstav_snitt = NUMBER_DICT[round(snitt)].upper()
        return render_template("result.html", snitt = tall_snitt, bokstav_snitt = bokstav_snitt, subjects = listify_subjects(subjects))
    return render_template("index.html", form = form)

if __name__ == "__main__":
    app.secret_key = SECRET
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
