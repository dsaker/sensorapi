from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.db import get_db
from json import loads

bp = Blueprint('sensors', __name__)


def get_sensor(id):
    """Get a sensor.
    Checks that the id exists
    :param id: id of sensor to get
    :return: the sensor
    :raise 404: if a sensor with the given id doesn't exist
    """
    sensor = (
        get_db()
        .execute(
            "SELECT s.id, sensorname, ht_alert, lt_alert, hh_alert, lh_alert, \
                temp_alert_on, hum_alert_on, time_between"
            " FROM temp_sensor s"
            " WHERE s.id = ?",
            (id,),
        )
        .fetchone()
    )

    if sensor is None:
        abort(404, "Sensor id {0} doesn't exist.".format(id))

    return sensor


@bp.route('/')
def index():
    db = get_db()
    sensors = db.execute(
        'SELECT *'
        ' FROM temp_sensor'
    ).fetchall()
    return render_template('sensors/index.html', sensors=sensors)


@bp.route('/create', methods=('POST',))
def create():
    """Create a new sensor when a sensor sends a post request with new sensorname."""
    if request.method == 'POST':
        content = loads(request.data)
        sensorname = content.get('sensorName')
        error = None

        if not sensorname:
            error = 'Sensor name is required.'

        if error is not None:
            flash(error)
        else:
            exists = (
                get_db()
                .execute(
                    "SELECT id, sensorname, ht_alert, lt_alert, hh_alert, lh_alert, \
                        temp_alert_on, hum_alert_on, time_between"
                    " FROM temp_sensor"
                    " WHERE sensorname = ?",
                    (sensorname,),
                )
                .fetchone()
            )
            if exists:
                return "sensorname already exists"
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
    sensor = get_sensor(id)

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
    get_sensor(id)
    db = get_db()
    db.execute("DELETE FROM temp_sensor WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("sensors.index"))
