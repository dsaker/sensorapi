from flask import Flask, request, jsonify
from datetime import datetime,timedelta
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

alertTriggered = datetime.now() - timedelta(hours=6)
highTempAlert = 90
lowTempAlert = 40

passfile = open('./../../data/words', 'r')
words = json.loads(passfile.read())
pas = words['pass']
phoneNumber = words['phone']
email = words['email']
passfile.close()

sms_gateway = phoneNumber + '@messaging.sprintpcs.com'

smtp = "smtp.gmail.com"
smtp_port = 587

def checkTemp(temp, sensorName, currentTime):
  global alertTriggered
  if((currentTime - alertTriggered).total_seconds()/3600.0 > 6) and int(temp) > highTempAlert:
    alertTriggered = currentTime
    server = smtplib.SMTP(smtp, smtp_port)
    server.starttls()
    server.login(email, pas)

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = sms_gateway

    msg['Subject'] = "Alert from LoveLifeSensors\n"
    body = sensorName + ': ' + temp + ' F'

    msg .attach(MIMEText(body, 'plain'))
    sms = msg.as_string()
    server.sendmail(email, sms_gateway, sms)

    server.quit()

app = Flask(__name__)

@app.route('/api', methods=["POST","GET"])
def post():
  if request.method=='POST':
    content = json.loads(request.data)
    sensorName = content.get('sensorName')
    temp = content.get('temp')
    currentTime = datetime.now()
    with open('./../../data/' + sensorName,  "a") as outfile:
      json.dump({"time" : str(currentTime), "temp" : temp}, outfile)
    checkTemp(temp, sensorName, currentTime)
    return str("Success")
  else:
    return str("simple_api_smtp is responding to your request")


if __name__ == "__main__":
  app.run(host='0.0.0.0')