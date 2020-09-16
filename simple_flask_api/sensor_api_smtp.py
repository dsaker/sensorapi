# This implementation will only work for one sensor 

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# time between alerts in hours
alertFrequency = 12

# set alert triggered back by alertFrequency
highTempTriggered = lowTempTriggered = highHumTriggered = lowHumTriggered = datetime.now() - timedelta(hours=alertFrequency)

# set high and low temp/humidity to receive text
highTempAlert = 90
lowTempAlert = 40
highHumAlert = 80
lowHumAlert = 30

# get hidden words from words file
passfile = open('./../../data/words', 'r')
words = json.loads(passfile.read())
pas = words['pass'] 
phoneNumber = words['phone'] #phone number to send alert text to
email = words['email'] #email to send smtp through
passfile.close()

# set sms_gateway for user (will change with multiple users)
sms_gateway = phoneNumber + '@messaging.sprintpcs.com'

smtp = "smtp.gmail.com"
smtp_port = 587


# sends a text explaining alert to phoneNumber from words
def sendSMTP(alertType, sensorName, alertNum):
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


def checkTempHum(temp, humidity, sensorName, currentTime):
  global highTempTriggered, lowTempTriggered, highHumTriggered, lowHumTriggered
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


app = Flask(__name__)

@app.route('/api', methods=["POST","GET"])
def post():
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
  else:
    return str("simple_api_smtp is responding to your request")


if __name__ == "__main__":
  app.run(host='0.0.0.0')