import psycopg2
import logging

DBUSERNAME = 'postgres'
DBHOST = 'postgres'
DBNAME = 'cyclone'
DBPASSWORD = 'cyclone'

conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" %
                        (DBNAME, DBUSERNAME, DBHOST, DBPASSWORD))

cur = conn.cursor()


def save_forecast_data(data):
    logging.debug("saving forecast type %s %s", type(data), data)
    q = "insert into cyclone_forecast(hour, lat, long, intensity) values(%s, %s, %s, %s)"
    for r in data:
        try:
            cur.execute(q, r)
        except Exception as e:
            conn.rollback()
            logging.error(
                "failed to save forecast entry, error %s entry %s", e, r)
    conn.commit()


def save_history_data(data):
    logging.debug("saving forecast type %s %s", type(data), data)
    q = "insert into cyclone_history(time, lat, long, intensity) values(%s, %s, %s, %s)"
    for r in data:
        try:
            cur.execute(q, r)
        except Exception as err:
            conn.rollback()
            logging.error("failed to save history entry %s err %s", r, err)
    conn.commit()
