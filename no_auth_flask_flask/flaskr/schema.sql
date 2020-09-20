DROP TABLE IF EXISTS temp_sensor;
DROP TABLE IF EXISTS numbers;
DROP TABLE IF EXISTS smtp_creds;

CREATE TABLE smtp_creds (
    gmail TEXT NOT NULL,
    pass TEXT NOT NULL
);

CREATE TABLE numbers (
    phonenumber TEXT NOT NULL,
    carrier TEXT NOT NULL
);

CREATE TABLE temp_sensor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensorname TEXT NOT NULL UNIQUE,
    ht_alert INTEGER DEFAULT 90 NOT NULL,
    lt_alert INTEGER DEFAULT 50 NOT NULL,
    hh_alert INTEGER DEFAULT 80 NOT NULL,
    lh_alert INTEGER DEFAULT 40 NOT NULL, 
    temp_alert_on INTEGER DEFAULT 1 NOT NULL,
    hum_alert_on INTEGER DEFAULT 1 NOT NULL,
    time_between INTEGER DEFAULT 1 NOT NULL,
    alert_triggered TEXT DEFAULT "0001-01-01 01:00:00.000000" NOT NULL
);