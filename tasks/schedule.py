from celery import Celery
from celery.schedules import crontab
import tasks
from tasks import app

app.conf.timezone = 'UTC'
app.conf.beat_schedule = {
    'get-cyclones-list-every-hour': {
        'task': 'tasks.extract_cyclones_list',
        'schedule': crontab(minute=0),
    },
    'get-cyclone-details-every-15-mins': {
        'task': 'tasks.extract_cyclone_details',
        'schedule': crontab(minute='*/15'), 
    },
    'save-forecast-details-every-15-mins': {
        'task': 'tasks.save_forecast_data',
        'schedule': crontab(minute='*/15'),
    },
    'save-history-details-every-15-mins': {
        'task': 'tasks.save_historic_data',
        'schedule': crontab(minute='*/15'),
    },
}
