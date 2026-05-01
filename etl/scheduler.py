import os
from celery import Celery
from celery.schedules import crontab
from etl.main import run_pipeline

# Configure Celery
# Typically, this will read from environment variables or Django settings later.
# For standalone ETL testing, we use a basic Redis broker if available.
redis_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
app = Celery('nifty100_etl', broker=redis_url)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Kolkata',
    enable_utc=False,
)

@app.task
def run_etl_task(sql_dump_path=None):
    """
    Celery task to run the complete ETL pipeline.
    """
    try:
        run_pipeline(sql_dump_path)
        return {"status": "success", "message": "ETL completed."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Schedule ETL tasks
app.conf.beat_schedule = {
    'run-nifty100-etl-daily': {
        'task': 'etl.scheduler.run_etl_task',
        'schedule': crontab(hour=2, minute=0),  # Run daily at 2:00 AM
        'kwargs': {'sql_dump_path': 'data/raw_dump.sql'}
    },
}
