from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from flaskr.db import get_db
from json import loads
from datetime import datetime, timedelta
from json import loads
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
bp = Blueprint('data', __name__)


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


def sendSMTP(alertType, sensorName, alertNum):
    """sends a text explaining alert to phonenumbers in database
    """
    server = smtplib.SMTP(smtp, smtp_port)
    server.starttls()
    server.login(email, pas)

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = sms_gateway

    msg['Subject'] = "Alert from LoveLifeSensors\n"
    body = alertType + sensorName + ' : ' + alertNum

    msg .attach(MIMEText(body, 'plain'))
    sms = msg.as_string()
    server.sendmail(email, sms_gateway, sms)

  server.quit()


def checkTempHum(temp, humidity, sensor, currentTime):
    """Check if the temperature or humitidty is higher or lower than the alerts
    set for the sensor. If alert is triggered check how long it has been since
    last alert has been sent and if that is longer than time between for sensor
    """
  # calculate how long since last alert has been triggered and if temp is higher or lower than alert set
  if((currentTime - highTempTriggered).total_seconds()/3600.0) > alertFrequency and int(temp) > highTempAlert:
    highTempTriggered = currentTime
    sendSMTP("High Temperature Alert : ", sensorName, temp)
  elif((currentTime - lowTempTriggered).total_seconds()/3600.0) > alertFrequency and int(temp) < lowTempAlert:
    lowTempTriggered = currentTime
    sendSMTP("Low Temperature Alert : ", sensorName, temp)
  # calculate how long since last alert has been triggered and if hum is higher or lower than alert set
  if((currentTime - highHumTriggered).total_seconds()/3600.0) > alertFrequency and int(humidity) > highHumAlert:
    highHumTriggered = currentTime
    sendSMTP("High Humidity Alert : ", sensorName, humidity)
  elif((currentTime - lowHumTriggered).total_seconds()/3600.0) > alertFrequency and int(humidity) < lowHumAlert:
    lowHumTriggered = currentTime
    sendSMTP("Low Humidity Alert : ", sensorName, humidity)


@bp.route("/data", methods=("POST",))
def data():
    """Accepts data from sensors.
    Appends it to file for that sensor.
    """
    if request.method=='POST':
        # have to load request.data because of how sensor sends data in IoT/WemosD1Sensor
        content = json.loads(request.data)
        sensorName = content.get('sensorName')
        temp = content.get('temp')
        humidity = content.get('humidity')
        currentTime = datetime.now()
        # append json object to data file
        with open('./../../data/' + sensorName,  "a+") as outfile:
        json.dump({"time" : str(currentTime), "temp" : temp, "humidity" : humidity}, outfile)
        checkTempHum(temp, humidity, sensorName, currentTime)
        return str("Success")


@bp.route('/smtp_creds', methods=('GET', 'POST'))
def smtp_creds():
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
            return redirect(url_for('sensors.index'))

    return render_template("data/smtp_creds.html", sensor=sensor)
