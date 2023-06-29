import os
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import task_utils

db = SQLAlchemy()
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

# Scantransfer's Routes (index,add,edit,delete)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'  # use my actual database URI
db = SQLAlchemy(app)

class ScanTransferRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Date)
    user_id = db.Column(db.Integer)
    study_subject_id = db.Column(db.String(80))
    scan_id = db.Column(db.Integer)
    destination = db.Column(db.String(80))
    transfer_needed_by = db.Column(db.Date)
    status = db.Column(db.String(80))
    comment = db.Column(db.String(200))

db.create_all()  # make sure to remove this line in production. 

#SCantransfer route's
@app.route('/')
def index():
    requests = ScanTransferRequest.query.all()
    return render_template('index.html', requests=requests)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        request = ScanTransferRequest(
            created_at=request.form['created_at'],
            user_id=request.form['user_id'],
            study_subject_id=request.form['study_subject_id'],
            scan_id=request.form['scan_id'],
            destination=request.form['destination'],
            transfer_needed_by=request.form['transfer_needed_by'],
            status=request.form['status'],
            comment=request.form['comment']
        )
        db.session.add(request)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    request = ScanTransferRequest.query.get_or_404(id)

    if request.method == 'POST':
        request.created_at=request.form['created_at']
        request.user_id=request.form['user_id']
        request.study_subject_id=request.form['study_subject_id']
        request.scan_id=request.form['scan_id']
        request.destination=request.form['destination']
        request.transfer_needed_by=request.form['transfer_needed_by']
        request.status=request.form['status']
        request.comment=request.form['comment']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', request=request)  #Edit afterwards

@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    request = ScanTransferRequest.query.get_or_404(id)
    db.session.delete(request)
    db.session.commit()
    return redirect(url_for('index'))