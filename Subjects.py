import os
from datetime import datetime
from flask import request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from app import app, db
from models import Study, Subject


class StudyForm(FlaskForm):
    cc_num = StringField('CC#', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    fund_dpa = StringField('Fund/DPA#', validators=[DataRequired()])
    criteria = StringField('Criteria', validators=[DataRequired()])
    pi_name = StringField('PI Name', validators=[DataRequired()])
    comments = TextAreaField('Comments')
    entered_by = StringField('Entered By', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/study', methods=['GET', 'POST'])
def add_study():
    form = StudyForm()
    if form.validate_on_submit():
        new_study = Study(
            cc_num=form.cc_num.data,
            name=form.name.data,
            fund_dpa=form.fund_dpa.data,
            criteria=form.criteria.data,
            pi_name=form.pi_name.data,
            comment=form.comments.data
        )
        db.session.add(new_study)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('studytable.html', form=form)


@app.route('/subjects', methods=['GET', 'POST'])
def subjects_index():
    subjects=Subject.query.all()
    return render_template('subjects.html', subjects=subjects)


@app.route('/add_subject', methods=('GET', 'POST'))
def add_subject():
    if request.method == 'POST':
        email = request.form['email']
        patient = request.form['patient']
        baseline_date = request.form['baseline_date']

        new_subject = Subject(
            email=email,
            patient=patient,
            baseline_date=baseline_date
        )
        db.session.add(new_subject)
        db.session.commit()
        return redirect(url_for('subjects_index'))
    return render_template('add.html')


@app.route('/edit_subject/<int:id>', methods=('GET', 'POST'))
def edit_subject(id):
    subject = Subject.query.get_or_404(id)

    if request.method == 'POST':
        subject.email = request.form['email']
        subject.patient = request.form['patient']
        subject.baseline_date = request.form['baseline_date']

        db.session.commit()
        return redirect(url_for('subjects_index'))

    return render_template('edit.html', subject=subject)


@app.route('/delete_subject/<int:id>', methods=('POST',))
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for('subjects_index'))


@app.route('/edit_study/<int:id>', methods=('GET', 'POST'))
def edit_study(id):
    study = Study.query.get_or_404(id)

    if request.method == 'POST':
        study.cc = request.form['CC']
        study.name = request.form['Name']
        study.fund_dpa = request.form['Fund/DPA#']
        study.criteria = request.form['Criteria']
        study.pi_name = request.form['PI Name']
        study.comments = request.form['Comments']
        study.entered_by = request.form['Entered By']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', study=study)


@app.route('/delete_study/<int:id>', methods=('POST',))
def delete_study(id):
    study = Study.query.get_or_404(id)
    db.session.delete(study)
    db.session.commit()
    return redirect(url_for('index'))
