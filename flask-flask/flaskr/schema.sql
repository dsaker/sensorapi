DROP TABLE IF EXISTS temp_sensor;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  phonenumbers TEXT
);

CREATE TABLE temp_sensor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creator_id INTEGER NOT NULL,
    sensorname TEXT NOT NULL UNIQUE,
    ht_alert INTEGER DEFAULT 90 NOT NULL,
    lt_alert INTEGER DEFAULT 50 NOT NULL,
    hh_alert INTEGER DEFAULT 80 NOT NULL,
    lh_alert INTEGER DEFAULT 40 NOT NULL, 
    temp_alert INTEGER DEFAULT 1 NOT NULL,
    hum_alert INTEGER DEFAULT 1 NOT NULL,
    time_between INTEGER NOT NULL,
    FOREIGN KEY (creator_id) REFERENCES user (id)
);