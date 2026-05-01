"""
ETL Scheduler - Schedule automatic ETL runs
"""

from celery.schedules import crontab
from celery import Celery

app = Celery()

# Schedule ETL tasks
app.conf.beat_schedule = {
    'extract-data-daily': {
        'task': 'etl.tasks.run_etl',
        'schedule': crontab(hour=0, minute=0),  # Run daily at midnight
    },
}
