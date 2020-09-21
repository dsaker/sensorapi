from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from flaskr.db import get_db, get_all
from json import loads
from datetime import datetime
from json import loads, dump
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

bp = Blueprint('contacts', __name__, url_prefix='/contacts')


@bp.route('/update')
def update():
    '''
    if request.method == 'POST':
        gmail = request.form['gmail']
        password = request.form['password']
        db = get_db()
        error = None

        if not gmail:
            error = 'Gmail is required.'
        elif not password:
            error = 'Password is required.'
        elif error is not none:
            flash(error)
        elif db.execute(
                'SELECT id FROM smtp_creds WHERE gmail = ?', (gmail,)
            ).fetchone() is not None:
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
    creds = get_all('smpt_creds')
    contacts = get_all('contacts')
    return render_template("contact/update.html", creds=creds, contacts=contacts)
