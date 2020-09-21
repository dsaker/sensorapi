import sqlite3
from werkzeug.exceptions import abort
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_all(tablename):
    """Get all of the rows from a table.
    :param tablename: the table you want to fetchall from
    :return: all rows in table (None if rows=0)
    """
    all_rows = (
        get_db()
        .execute(
            "SELECT * FROM " + tablename
        )
        .fetchall()
    )

    return all_rows


def get_sensor_by_name(sensorname):
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


def get_sensor_by_id(id):
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
