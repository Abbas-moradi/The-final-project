from celery import Celery
from datetime import timedelta
import os


os.environ.setdefault('DJANGO_SETTING_MADULE', 'OnlineShop.setting')

celery_app = Celery('OnlineShop')
celery_app.autodiscover_tasks()

celery_app.conf.broker_url = 'redis://localhost:6379/0'
celery_app.conf.result_backend = 'redis://localhost:6379/1'
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'json'
celery_app.conf.accept_content = ['json', 'json']
celery_app.conf.result_expires = timedelta(seconds=1)
celery_app.conf.tasks_always_eager = False
celery_app.conf.worker_prefetch_multiplier = 4