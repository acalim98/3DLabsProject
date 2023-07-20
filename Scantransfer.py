import os
import datetime
import sqlite3
from sqlite3 import Error
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template
from flask_login import UserMixin, login_user
from app import app, db
from models import User, ScanTransferRequest


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(':memory:')  # creates a RAM database for demo purposes
        return conn
    except Error as e:
        print(e)


@app.route('/submit_patient_info', methods=['POST'])
def submit_patient_info():
    # Handle patient info submission here
    pass


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


@app.route('/ScanTransferIndex')
def index():
    requests = ScanTransferRequest.query.all()
    return render_template('scantransfer.html', requests=requests)


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
        request.created_at = request.form['created_at']
        request.user_id = request.form['user_id']
        request.study_subject_id = request.form['study_subject_id']
        request.scan_id = request.form['scan_id']
        request.destination = request.form['destination']
        request.transfer_needed_by = request.form['transfer_needed_by']
        request.status = request.form['status']
        request.comment = request.form['comment']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', request=request)


@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    request = ScanTransferRequest.query.get_or_404(id)
    db.session.delete(request)
    db.session.commit()
    return redirect(url_for('index'))
