import os
import time

from celery import Celery
from pizzaweb import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pizzaweb.settings")
app = Celery("pizzaweb")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

@app.task()
def test_task():
    time.sleep(20)
    print('hello selery')