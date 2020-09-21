from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify
)
from flaskr.db import (
    get_db, get_sensor_by_name, get_all, update_sensor
)
from datetime import datetime
from json import loads, dump
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

bp = Blueprint('temp_sensor', __name__)
smtp = "smtp.gmail.com"
smtp_port = 587


def sendSMTP(alert_type, sensorname, alert_val):
    """sends a text explaining alert to phonenumbers in database
    """
    server = SMTP(smtp, smtp_port)
    server.starttls()
    creds = get_all('smtp_creds')
    email = creds['gmail']
    server.login(email, creds['password'])

    contacts = get_all('contacts')

    for row in contacts:

        sms_gateway = row.number['phonenumber'] + row.number['carrier']

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = sms_gateway

        msg['Subject'] = "Alert from SimpleSensors\n"
        body = alert_type + sensorname + ' : ' + alert_val

        msg.attach(MIMEText(body, 'plain'))
        sms = msg.as_string()
        server.sendmail(email, sms_gateway, sms)

        server.quit()


def checkTempHum(temp, humidity, sensorname, current_time):
    """Check if the temperature or humitidty is higher or lower than the alerts
    set for the sensor. If alert is triggered check how long it has been since
    last alert has been sent and if that is longer than time between for sensor
    :param temp, humidity, sensorname, current_time
    :return: None
    """
    sensor = get_sensor_by_name(sensorname)
    # fetch last alert triggered, convert to datetime (0001-01-01 01:00:00.000000)
    last_triggered = datetime.strptime(sensor["alert_triggered"], '%Y-%m-%d %H:%M:%S.%f')
    # see if alert has been triggered since amount of time set between alerts
    trigger = (current_time - last_triggered).total_seconds()/3600.0 > sensorname['time_between']
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
        elif int(humidity) < sensor['lh_alert']:
            update_triggered = True
            sendSMTP("Low Humidity Alert : ", sensorname, humidity)
    if update_triggered:
        update_sensor('last_triggered', str(current_time), sensor['id'])


@bp.route("/temp_sensor", methods=("POST",))
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
        checkTempHum(temp, humidity, sensorName, currentTime)
