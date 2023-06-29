import os
import datetime
from datetime import date
import time

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


    return render_template('login.html')
if __name__ == '__main__':
    app.run(debug=True)

#Subjects funtions
app = Flask(__name__)

DATABASE = 'my_database.db'  # your SQLite database file path


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    subjects = conn.execute('SELECT * FROM subjects').fetchall()
    conn.close()
    return render_template('index.html', subjects=subjects)


@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        email = request.form['email']
        patient = request.form['patient']
        baseline_date = request.form['baseline_date']

        conn = get_db_connection()
        conn.execute('INSERT INTO subjects (email, patient, baseline_date) VALUES (?, ?, ?)',
                     (email, patient, baseline_date))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    subject = conn.execute('SELECT * FROM subjects WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        email = request.form['email']
        patient = request.form['patient']
        baseline_date = request.form['baseline_date']

        conn.execute('UPDATE subjects SET email = ?, patient = ?, baseline_date = ? WHERE id = ?',
                     (email, patient, baseline_date, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('edit.html', subject=subject)


@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM subjects WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

 #Study table routes

 @app.route('/')
def index():
    conn = get_db_connection()
    studies = conn.execute('SELECT * FROM studies').fetchall()
    conn.close()
    return render_template('index.html', studies=studies)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        cc = request.form['CC']
        name = request.form['Name']
        fund_dpa = request.form['Fund/DPA#']
        criteria = request.form['Criteria']
        pi_name = request.form['PI Name']
        comments = request.form['Comments']
        entered_by = request.form['Entered By']

        conn = get_db_connection()
        conn.execute('INSERT INTO studies (cc, name, fund_dpa, criteria, pi_name, comments, entered_by) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (cc, name, fund_dpa, criteria, pi_name, comments, entered_by))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    study = conn.execute('SELECT * FROM studies WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        cc = request.form['CC']
        name = request.form['Name']
        fund_dpa = request.form['Fund/DPA#']
        criteria = request.form['Criteria']
        pi_name = request.form['PI Name']
        comments = request.form['Comments']
        entered_by = request.form['Entered By']

        conn.execute('UPDATE studies SET cc = ?, name = ?, fund_dpa = ?, criteria = ?, pi_name = ?, comments = ?, entered_by = ? WHERE id = ?',
                     (cc, name, fund_dpa, criteria, pi_name, comments, entered_by, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('edit.html', study=study)

@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM studies WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
