from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from flaskr.db import get_db
from json import loads
from datetime import datetime
from json import loads, dump
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

bp = Blueprint('contact', __name__, url_prefix='/contact')
smtp = "smtp.gmail.com"
smtp_port = 587


def get_sensor(sensorname):
    """Get a sensor.
    Checks that the sensorname exists
    :param sensorname: sensorname of sensor to get
    :return: the sensor
    :raise 404: if a sensor with the given sensorname doesn't exist
    """
    sensor = (
        get_db()
        .execute(
            "SELECT id, sensorname, ht_alert, lt_alert, hh_alert, lh_alert, \
                temp_alert_on, hum_alert_on, time_between, alert_triggered"
            " FROM temp_sensor s"
            " WHERE sensorname = ?",
            (sensorname,),
        )
        .fetchone()
    )

    if sensor is None:
        abort(404, "Sensor sensorname {0} doesn't exist.".format(sensorname))

    return sensor

def get_numbers():
    """Get all of the numbers to receive alerts.
    :param None: you want to return all rows so fetchall
    :return: all rows in numbers table
    :raise 404: if no numbers exist
    """
    numbers = (
        get_db()
        .execute(
            "SELECT *"
            "FROM numbers"
        )
        .fetchall()
    )

    if numbers is None:
        abort(404, "Numbers to contact do not exist. Please add.")

    return numbers


def get_smtp_creds():
    """Get a smtp creds. There should only be one so only fetchone.
    Checks that the smtp_creds exist
    :param None: there should only be one
    :return: the credentials
    :raise 404: if no credential exist
    """
    creds = (
        get_db()
        .execute(
            "SELECT *"
            "FROM smtp_creds"
        )
        .fetchone()
    )

    if creds is None:
        abort(404, "SMTP Credentials do not exist. Please add.")

    return creds


def sendSMTP(alert_type, sensorname, alert_val):
    """sends a text explaining alert to phonenumbers in database
    """
    server = smtplib.SMTP(smtp, smtp_port)
    server.starttls()
    creds = get_smtp_creds
    email = creds['gmail']
    server.login(email, creds['password'])

    numbers_table = get_numbers()

    for row in numbers_table:

        sms_gateway = row.number['phonenumber'] + number['carrier']

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = sms_gateway

        msg['Subject'] = "Alert from SimpleSensors\n"
        body = alert_type + sensorname + ' : ' + alert_val

        msg.attach(MIMEText(body, 'plain'))
        sms = msg.as_string()
        server.sendmail(email, sms_gateway, sms)

        server.quit()


def update_sensor(column, value, id):
    """Update the temp_sensor table column with the value
    :param column: the column of temp_sensor to be updated
    :param value: the value to be updated to
    :param id: the id of the temp_sensor to be updated
    :return: None
    """
    db = get_db()
    db.execute(
        "UPDATE temp_sensor SET " + column  + " = ?"
        "WHERE id = ?", 
        (value, id)
    )
    db.commit()


def checkTempHum(temp, humidity, sensorname, current_time):
    """Check if the temperature or humitidty is higher or lower than the alerts
    set for the sensor. If alert is triggered check how long it has been since
    last alert has been sent and if that is longer than time between for sensor
    :param temp, humidity, sensorname, current_time
    :return: None
    """
    sensor = get_sensor(sensorname)
    # fetch last alert triggered, convert to datetime (0001-01-01 01:00:00.000000)
    last_triggered = datetime.strptime(sensor["alert_triggered"], '%Y-%m-%d %H:%M:%S.%f')
    # see if alert has been triggered since amount of time set between alerts
    trigger = (current_time - last_triggered).total_seconds()/3600.0 > sensorName['time_between']
    update_triggered = False
    if trigger:
        if int(temp) > sensor['ht_alert']:
            update_triggered = True
            sendSMTP("High Temperature Alert : ", sensorname, temp)
        elif int(temp) < sensor['lt_alert']:
            update_triggered = True
            sendSMTP("Low Temperature Alert : ", sensorname, temp)
        if int(humidity) > sensor['hh_alert']:
            update_triggered = True
            sendSMTP("High Humidity Alert : ", sensorname, humidity)
        elif int(humidity) < sensorName['lh_alert']:
            update_triggered = True
            sendSMTP("Low Humidity Alert : ", sensorname, humidity)
    if update_triggered:
        update_sensor('last_triggered', str(current_time), sensor['id'])

@bp.route("/data", methods=("POST",))
def data():
    """Accepts data from sensors.
    Appends it to file for that sensor.
    """
    if request.method=='POST':
        # have to load request.data because of how sensor sends data in IoT/WemosD1Sensor
        content = loads(request.data)
        sensorName = content.get('sensorName')
        temp = content.get('temp')
        humidity = content.get('humidity')
        currentTime = datetime.now()
        # append json object to data file
        with open('./../data/' + sensorName,  "a+") as outfile:
            dump({"time" : str(currentTime), "temp" : temp, "humidity" : humidity}, outfile)
        sensorname = checkTempHum(temp, humidity, sensorName, currentTime)
        return sensorname


@bp.route('/update')
def update(creds):
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

    return render_template("contact/update.html", creds=creds)
