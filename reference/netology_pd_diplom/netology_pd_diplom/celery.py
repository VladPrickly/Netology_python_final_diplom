import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netology_pd_diplom.settings')

app = Celery(
    'netology_pd_diplom',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Расширенная статистика для Flower
app.conf.update(
    worker_send_task_events=True,  # Отправлять события задач
    task_send_sent_event=True,     # Отправлять событие отправки
)