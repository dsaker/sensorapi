from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.db import (
    get_db, get_sensor_by_id, get_sensor_by_name, get_all
)
from json import loads

bp = Blueprint('sensors', __name__)


@bp.route('/')
def index():
    sensors = get_all('temp_sensor')
    creds = get_all('smtp_creds')
    contacts = get_all('contacts')
    return render_template('sensors/index.html', sensors=sensors, creds=creds, contacts=contacts)


@bp.route('/create', methods=('POST',))
def create():
    """Create a new sensor sends a post request with new sensorname."""
    if request.method == 'POST':
        content = loads(request.data)
        sensorname = content.get('sensorName')
        error = None

        if not sensorname:
            error = 'Sensor name is required.'

        if error is not None:
            flash(error)
        else:
            exists = get_sensor_by_name('sensorName')
            if exists:
                return "Sensorname already exists"
            else:
                db =  get_db()
                db.execute(
                    'INSERT INTO temp_sensor (sensorname)'
                    ' VALUES (?)',
                    (sensorname,)
                )
                db.commit()
                return "sensor created"


@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    """Update a sensor."""
    sensor = get_sensor_by_id(id)

    if request.method == "POST":
        sensorname = request.form['sensorname']
        ht_alert = request.form['ht_alert']
        lt_alert = request.form['lt_alert']
        hh_alert = request.form['hh_alert']
        lh_alert = request.form['lh_alert']
        temp_alert = request.form['temp_alert']
        hum_alert = request.form['hum_alert']
        time_between = request.form['time_between']
        error = None

        if not sensorname:
            error = "Sensor name is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE temp_sensor SET sensorname = ?, ht_alert = ?, lt_alert = ?, \
                 hh_alert = ?, lh_alert = ?, temp_alert_on = ?, hum_alert_on = ?, \
                 time_between = ? WHERE id = ?", (sensorname, ht_alert, 
                    lt_alert, hh_alert, lh_alert, temp_alert, hum_alert, 
                    time_between, id)
            )
            db.commit()
            return redirect(url_for("sensors.index"))

    return render_template("sensors/update.html", sensor=sensor)


@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    """Delete a sensor.
    Ensures that the sensor exists.
    """
    db = get_db()
    db.execute("DELETE FROM temp_sensor WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("sensors.index"))
