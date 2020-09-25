from celery import Celery
from celery.utils.log import get_task_logger
from kombu import Connection
import logging
import os
import sys

log = get_task_logger(__name__)
h = logging.StreamHandler(sys.stdout)
log.addHandler(h)

sys.path.append(os.getcwd() + "/..")

from scraper import scraper
from repo import db_repo


CYCLONE_LIST_QUEUE = 'cyclones.list'
CYCLONE_DETAILS_QUEUE = 'cyclones.details'
CYCLONE_HISTORY_QUEUE = "cyclone.history"
CYCLONE_FORECAST_QUEUE = "cyclone.forecast"

BROKER_URL = "redis://redis"

kombu_conn = Connection(BROKER_URL)

list_queue = kombu_conn.SimpleQueue(CYCLONE_LIST_QUEUE)
details_queue = kombu_conn.SimpleQueue(CYCLONE_DETAILS_QUEUE)
history_queue = kombu_conn.SimpleQueue(CYCLONE_HISTORY_QUEUE)
forecast_queue = kombu_conn.SimpleQueue(CYCLONE_FORECAST_QUEUE)

CELERY_BROKER_URL = 'redis://redis'

app = Celery('tasks', broker=CELERY_BROKER_URL)


@app.task
def extract_cyclones_list():
    log.info("extract list of cyclones")
    cyclones = scraper.extract_cyclones_list()
    for c in cyclones:
        log.info("adding %s", c)
        list_queue.put(c)

    log.info("list enquing ok")


@app.task
def extract_cyclone_details():
    log.info("extracting cyclone details")
    message = ""
    try:
        message = list_queue.get(block=False, timeout=1)
    except Exception as e:
        log.error("unable to get cyclones list %s", e)
        return

    data = scraper.extract_cyclone_details(message.payload)
    message.ack()

    history_data = data['history']
    history_queue.put(history_data)

    forecast_data = data['forecast']
    forecast_queue.put(forecast_data)


@app.task
def save_forecast_data():
    log.info("saving forecast data...")
    forecast_data = []
    try:
        forecast_data = forecast_queue.get(block=False, timeout=1)
    except Exception as e:
        log.error("unable to get forecast %s", e)
        return

    log.info("saving forecast data %s", forecast_data.payload)
    db_repo.save_forecast_data(list(forecast_data.payload))
    forecast_data.ack()


@app.task
def save_historic_data():
    log.info("saving historic data ...")
    historic_data = []
    try:
        historic_data = history_queue.get(block=False, timeout=1)
    except Exception as e:
        log.error("unable to get historic %s", e)
        return

    log.info("saving historic data %s", historic_data.payload)
    db_repo.save_history_data(list(historic_data.payload))
    historic_data.ack()
