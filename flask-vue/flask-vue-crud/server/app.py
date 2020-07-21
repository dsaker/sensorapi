import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS


SENSORS = [
    {
        'id': uuid.uuid4().hex,
        'name': 'practice1',
        'HTAlert': '90',
        'LTAlert': '50',
        'HHAlert': '70',
        'LHAlert': '30',
        'TempAlertOn': True,
        'HumAlertOn': True
    },
    {
        'id': uuid.uuid4().hex,
        'name': 'practice2',
        'HTAlert': '90',
        'LTAlert': '50',
        'HHAlert': '70',
        'LHAlert': '30',
        'TempAlertOn': True,
        'HumAlertOn': True
    },
    {
        'id': uuid.uuid4().hex,
        'name': 'practice3',
        'HTAlert': '90',
        'LTAlert': '50',
        'HHAlert': '70',
        'LHAlert': '30',
        'TempAlertOn': True,
        'HumAlertOn': True
    }
]

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def remove_sensor(sensor_id):
    for sensor in SENSORS:
        if sensor['id'] == sensor_id:
            SENSORS.remove(sensor)
            return True
    return False


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/sensors', methods=['GET', 'POST'])
def all_sensors():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        SENSORS.append({
            'id': uuid.uuid4().hex,
            'name': post_data.get('name'),
            'HTAlert': post_data.get('HTAlert'),
            'LTAlert': post_data.get('LTAlert'),
            'HHAlert': post_data.get('HHAlert'),
            'LHAlert': post_data.get('LHAlert'),
            'TempAlertOn': post_data.get('TempAlertOn'),
            'HumAlertOn': post_data.get('HumAlertOn')
        })
        response_object['message'] = 'sensor added!'
    else:
        response_object['sensors'] = SENSORS
    return jsonify(response_object)


@app.route('/sensors/<sensor_id>', methods=['PUT', 'DELETE'])
def single_sensor(sensor_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_sensor(sensor_id)
        SENSORS.append({
            'id': uuid.uuid4().hex,
            'name': post_data.get('name'),
            'HTAlert': post_data.get('HTAlert'),
            'LTAlert': post_data.get('LTAlert'),
            'HHAlert': post_data.get('HHAlert'),
            'LHAlert': post_data.get('LHAlert'),
            'TempAlertOn': post_data.get('TempAlertOn'),
            'HumAlertOn': post_data.get('HumAlertOn')
        })
        response_object['message'] = 'sensor updated!'
    if request.method == 'DELETE':
        remove_sensor(sensor_id)
        response_object['message'] = 'sensor removed!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()