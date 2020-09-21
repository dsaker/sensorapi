from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from flaskr.db import get_db, get_all, get_smtp_by_id
from json import loads
from datetime import datetime
from json import loads, dump
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

bp = Blueprint('contacts', __name__, url_prefix='/contacts')


@bp.route('/update')
def update():

    creds = get_all('smtp_creds')
    contacts = get_all('contacts')
    return render_template("contacts/update.html", creds=creds, contacts=contacts)

@bp.route('/<int:id>/update_smtp', methods=("GET", "POST"))
def update_smtp():
    '''update smtp credentials'''
    creds = get_smtp_by_id(id)

    if request.method == 'POST':
        gmail = request.form['gmail']
        password = request.form['password']
        error = None

        if not gmail:
            error = 'Gmail is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is not none:
            flash(error)
        else:
            db = get_db()
                db.execute(
                    "UPDATE smtp_creds SET gmail = ?, password = ?", 
                    (gmail, password)
                )
                db.commit()
                return redirect(url_for('sensors.index'))
        else:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('sensors.index'))'''
    creds = get_all('smtp_creds')
    contacts = get_all('contacts')
    return render_template("contacts/update.html", creds=creds, contacts=contacts)