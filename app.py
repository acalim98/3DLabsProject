import os
import datetime
from datetime import date
import time
from flask import Flask, render_template, request, url_for, redirect
from markupsafe import escape
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import Optional
import sqlite3
from sqlite3 import Error
from flask_login import UserMixin


# Flask app for web
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# create instance of database object
db = SQLAlchemy(app)
#db.init_app(app)

# create Todo table in database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    new = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f'<Todo {self.id}>'

    def add_random_todos():
        for _ in range(10):
            new_todo = Todo(content=f'Task with ID')
            db.session.add(new_todo)

    db.session.commit()

@app.route("/add_random_todos")
def add_random_todos_route():
    add_random_todos()
    return "Added 10 random todos."

@app.route("/create_db")
def create_db():
    with app.app_context():
        db.create_all()

    return "Database created."

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/base")
def base():
    return render_template('base.html')

@app.route("/example")
def example():
    text = 'Hello, World! This is an example page!'
    return render_template('example.html', text=text)

@app.route("/link")
def my_link():
    my_link_text = "This is a link!"
    return render_template('example_link.html', text=my_link_text)

@app.route('/todos', methods=['GET', 'POST'])
def todos():
    todos = Todo.query.all()
    return render_template('todos.html', todos=todos)

@app.route('/todos/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if request.method == 'POST':
        todo.content = request.form['content']
        db.session.commit()
        return redirect(url_for('todos'))
    return render_template('edit_todo.html', todo=todo)

@app.route('/todos/delete/<int:todo_id>')
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todos'))

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



class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    study_id = db.Column(db.Integer, nullable=False)
    patient_id = db.Column(db.Integer, nullable=False)
    baseline_date = db.Column(db.Date, nullable=True)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    dummy_int = db.Column(db.Integer, nullable=True)





class Study(db.Model):
    __tablename__ = 'studies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    fund_dpa = db.Column(db.String(255), nullable=False)
    criteria = db.Column(db.String(255), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    cc_num = db.Column(db.String(255), nullable=False)
    pi_name = db.Column(db.String(255), nullable=False)
    # and so on for the rest of your columns...

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
            comment=form.comments.data,
            # and so on for the rest of your columns...
        )
        db.session.add(new_study)
        db.session.commit()
        return redirect(url_for('study_success'))
    return render_template('studytable.html', form=form)

def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect(':memory:') # creates a RAM database for demo purposes
        return conn
    except Error as e:
        print(e)

@app.route('/submit_patient_info', methods=['POST'])
def submit_patient_info():
    first_name = request.form


def create_table(conn):
    try:
        sql = '''CREATE TABLE Scan_transfers (
                    id INTEGER PRIMARY KEY,
                    scan_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    study_subject_id TEXT,
                    study_timepoint TEXT,
                    destination TEXT,
                    destination_other_detail TEXT,
                    transfer_needed_by DATE,
                    comment TEXT,
                    transfer_date DATE,
                    transfer_by INTEGER,
                    transfer_method TEXT,
                    transfer_method_other_detail TEXT,
                    status TEXT,
                    retransfer_date DATE,
                    retransfer_reason TEXT,
                    has_been_billed BOOLEAN,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                );'''
        cur = conn.cursor()
        cur.execute(sql)
        print("Table created successfully")
    except Error as e:
        print(e)

def main():
    conn = create_connection()
    if conn is not None:
        create_table(conn)
    else:
        print("Error! Cannot create the database connection.")
        

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(255))
    email = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    role = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    is_active = db.Column(db.String(255))
    is_admin = db.Column(db.Integer, default=0)
    is_radiologist = db.Column(db.Integer, default=0)
    is_developer = db.Column(db.Integer, default=0)
    is_coordinator = db.Column(db.Integer, default=0)
    is_pi = db.Column(db.Integer, default=0)
    is_finance = db.Column(db.Integer, default=0)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return redirect(url_for('login'))

        login_user(user)

        return redirect(url_for('profile'))

    return render_template('login.html')
if __name__ == '__main__':
    app.run(debug=True)
