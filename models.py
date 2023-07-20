from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db

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
  

    #Login DB
    
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    mrn = db.Column(db.String(20), unique=True, nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    comments = db.Column(db.Text)

#Scan Trans DB

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

