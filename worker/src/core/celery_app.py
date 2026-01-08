import os
from celery import Celery

celery_app = Celery('worker',
             broker=os.getenv('CELERY_BROKER_URL'),
             include=['src.tasks'])  # Для автодискавери задач

celery_app.conf.update(
    task_default_queue='notifications',
    task_acks_late=True,  # Ack после выполнения, т.е. при сбое задача вернётся в очередь
    worker_prefetch_multiplier=1,  # Выбирать по одной задаче за раз
    task_time_limit=30,  # Максимальное время выполнения задачи в секундах
    broker_transport_options={'visibility_timeout': 3600}  # Для Redis
)
