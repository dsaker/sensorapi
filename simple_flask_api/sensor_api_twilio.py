from flask import Flask, request, jsonify
from datetime import datetime,timedelta
import json
from twilio.rest import Client

alertTriggered = datetime.now() - timedelta(hours=6)
highTempAlert = 90
lowTempAlert = 40

def checkTemp(temp, sensorName, currentTime):
  if((currentTime - alertTriggered).total_seconds()/3600.0 > 6):
    
    twilfile = open('./../../data/words', 'r')
    words = json.loads(twilfile.read())

    client = Client(words['SID'], words['token'])
    message = client.messages.create(
      from_ = words['fromNum'],
      body = sensorName + ' ' + str(currentTime) + ' ' + temp + ' F',
      to = words['toNum']
    )
    
    print(message.sid)

    twilfile.close()

app = Flask(__name__)

@app.route('/api', methods=["POST","GET"])
def post():
  if request.method=='POST':
    content = request.get_json()
    sensorName = content.get('sensorName')
    temp = content.get('temp')
    currentTime = datetime.now()
    with open('./../../data/' + sensorName,  "a") as outfile:
      json.dump({"time" : str(currentTime), "temp" : temp}, outfile)
    checkTemp(temp, sensorName, currentTime)
    return jsonify(str("Success"))
  else:
    return jsonify(str("simple_api_twilio is responding to your request"))

if __name__ == "__main__":
  app.run(host='0.0.0.0')