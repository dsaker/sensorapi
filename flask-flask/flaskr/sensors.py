from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('sensors', __name__)

@bp.route('/')
def index():
    db = get_db()
    sensors = db.execute(
        'SELECT *'
        ' FROM temp_sensor s JOIN user u ON s.creator_id = u.id'
    ).fetchall()
    return render_template('sensors/index.html', sensors=sensors)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
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
            error = 'Sensor name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO temp_sensor (sensorname, ht_alert, lt_alert, hh_alert, \
                    lh_alert, temp_alert_on, hum_alert_on, time_between_alerts, creator_id)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (sensorname, ht_alert, lt_alert, hh_alert,
                    lh_alert, temp_alert, hum_alert, time_between, g.user["id"])
            )
            db.commit()
            return redirect(url_for('sensor.index'))
sensorname, ht_alert, lt_alert, hh_alert,
                    lh_alert, temp_alert, hum_alert, time_between
    return render_template('sensors/create.html')


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a sensor if the current user is the author."""
    post = get_post(id)

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
                "UPDATE post SET sensorname = ?, ht_alert = ?, lt_alert = ? \
                 hh_alert = ?, lh_alert = ? temp_alert_on = ? hum_alert_on = ? \
                 time_between_alerts = ? WHERE id = ?", (sensorname, ht_alert, 
                    lt_alert, hh_alert, lh_alert, temp_alert, hum_alert, 
                    time_between, id)
            )
            db.commit()
            return redirect(url_for("sensors.index"))

    return render_template("sensors/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a sensor.
    Ensures that the sensor exists and that the logged in user is the
    creator of the sensor.
    """
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))
