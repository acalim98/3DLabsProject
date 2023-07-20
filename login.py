import os
from datetime import datetime
from flask import request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from app import app
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators, TextAreaField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Optional
from models import db, Patient

class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/create_db")
def create_db():
    with app.app_context():
        db.create_all()
    return "Database created."

@app.route("/")
def base():
    return render_template('base.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = MyForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            message = form.message.data
            return redirect(url_for('success'))
    return render_template('form.html', form=form)


@app.route('/success')
def success():
    return 'Form submitted successfully!'


class SubjectInfoForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired()])
    patient = SelectField('Patient:', choices=[('', 'Name'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')])
    baseline_date = DateField('Baseline Date:', validators=[DataRequired()])
    submit = SubmitField('Save Changes')

'''
@app.route('/', methods=['GET', 'POST'])
def subject_info():
    form = SubjectInfoForm()
    if form.validate_on_submit():
        # You can process the form data here
        return redirect(url_for('subject_info'))
    return render_template('subject_info.html', form=form) 
'''


class PatientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    mrn = StringField('MRN', validators=[DataRequired()])
    birthdate = DateField('Birthdate', validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[Optional()])
    submit = SubmitField('Save Changes')


@app.route('/patient', methods=['GET', 'POST'])
def patient():
    form = PatientForm()
    if form.validate_on_submit():
        comment = form.comment.data if form.comment.data else None
        new_patient = Patient(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            mrn=form.mrn.data,
            birthdate=form.birthdate.data,
            comments=comment
        )
        db.session.add(new_patient)
        db.session.commit()
        return redirect(url_for('patientindex'))
    return render_template('new_patient.html', form=form)


@app.route('/patient/edit/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if request.method == 'POST':
        # You should replace 'content' with the actual attribute you want to change in the 'Patient' model
        patient.content = request.form['content']
        db.session.commit()
        return redirect(url_for('patient'))
    return render_template('editpatient.html', patient=patient)


@app.route('/patientindex', methods=['GET', 'POST'])
def patientindex():
    patients = Patient.query.all()
    return render_template('patientindex.html', patients=patients)


@app.route('/patient_success')
def patient_success():
    return 'Patient information saved successfully!'


@app.route('/add', methods=['POST'])
def add_patient():
    patient = Patient(
        first_name=request.form.get('first_name'),
        last_name=request.form.get('last_name'),
        mrn=request.form.get('mrn'),
        birthdate=datetime.strptime(request.form.get('birthdate'), '%Y-%m-%d').date(),
        comments=request.form.get('comments')
    )
    db.session.add(patient)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:id>', methods=['POST'])
def delete_patient(id):
    patient = Patient.query.get(id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('index'))
