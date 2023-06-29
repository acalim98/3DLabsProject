import os
from flask_sqlalchemy import SQLAlchemy

class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')

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

#@app.route('/', methods=['GET', 'POST'])
#def subject_info():
   # form = SubjectInfoForm()
   # if form.validate_on_submit():
        # You can process the form data here
       # return redirect(url_for('subject_info'))
    #return render_template('subject_info.html', form=form) 


@app.route('/patient', methods=['GET', 'POST'])
def patient():
    form = PatientForm()
    if form.validate_on_submit():
        new_patient = Patient(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            mrn=form.mrn.data,
            birthdate=form.birthdate.data,
            comment=form.comment.data
        )
        db.session.add(new_patient)
        db.session.commit()
        return redirect(url_for('patient_success'))
    return render_template('newpatient.html', form=form)

@app.route('/patient/edit/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if request.method == 'POST':
        patient.content = request.form['content']
        db.session.commit()
        return redirect(url_for('patient'))
    return render_template('editpatient.html', patient=patient)

@app.route('/patientindex', methods=['GET', 'POST'])
def patientindex():
    patients = Patient.query.all()
    return render_template('patientindex.html', patients=patients)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    mrn = db.Column(db.String(255), nullable=False)
    birthdate = db.Column(db.Date)
    comment = db.Column(db.Text)


class PatientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    mrn = StringField('MRN', validators=[DataRequired()])
    birthdate = DateField('Birthdate', validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[Optional()])
    submit = SubmitField('Save Changes')


@app.route('/patient_success')
def patient_success():
    return 'Patient information saved successfully!'

#Login Routes 

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    mrn = db.Column(db.String(20), unique=True, nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    comments = db.Column(db.Text)

db.create_all()  # make sure to remove this line in production!

@app.route('/')
def index():
    patients = Patient.query.all()
    return render_template('index.html', patients=patients)

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

@app.route('/edit/<int:id>', methods=['POST'])
def edit_patient(id):
    patient = Patient.query.get(id)
    patient.first_name = request.form.get('first_name')
    patient.last_name = request.form.get('last_name')
    patient.mrn = request.form.get('mrn')
    patient.birthdate = datetime.strptime(request.form.get('birthdate'), '%Y-%m-%d').date()
    patient.comments = request.form.get('comments')
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_patient(id):
    patient = Patient.query.get(id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('index'))

#edit patient routes "adjustments needed"

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    mrn = db.Column(db.String(20), unique=True, nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    comments = db.Column(db.Text)

db.create_all()  # REmove this line in production!!

@app.route('/', methods=['GET'])
def index():
    patients = Patient.query.all()
    return render_template('index.html', patients=patients)  # Update to your template

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

@app.route('/editpatient', methods=['POST'])
def edit_patient():
    id = request.form.get('id')
    patient = Patient.query.get(id)
    patient.first_name = request.form.get('first_name')
    patient.last_name = request.form.get('last_name')
    patient.mrn = request.form.get('mrn')
    patient.birthdate = datetime.strptime(request.form.get('birthdate'), '%Y-%m-%d').date()
    patient.comments = request.form.get('comments')
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_patient(id):
    patient = Patient.query.get(id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('index'))

