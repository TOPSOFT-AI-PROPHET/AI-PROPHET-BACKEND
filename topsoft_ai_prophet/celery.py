import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "topsoft_ai_prophet.settings")
app = Celery("topsoft_ai_prophet")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
