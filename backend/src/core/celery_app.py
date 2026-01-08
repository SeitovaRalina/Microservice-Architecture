import os
from celery import Celery

celery_app = Celery(
    'backend',
    broker=os.getenv('CELERY_BROKER_URL'),
)

celery_app.conf.update(
    task_default_queue='notifications',
    task_queues={
        'notifications': {'exchange': 'notifications', 'routing_key': 'notifications'},
        'moderation': {'exchange': 'moderation', 'routing_key': 'moderation'},
        'preview': {'exchange': 'preview', 'routing_key': 'preview'},
        'publish': {'exchange': 'publish', 'routing_key': 'publish'},
        'dlq': {'exchange': 'dlq', 'routing_key': 'dlq'},
    },
    task_acks_late=True,  # Ack после выполнения, т.е. при сбое задача вернётся в очередь
    worker_prefetch_multiplier=1,  # Выбирать по одной задаче за раз
    task_time_limit=60,  # Максимальное время выполнения задачи в секундах
    broker_transport_options={'visibility_timeout': 3600}
)
