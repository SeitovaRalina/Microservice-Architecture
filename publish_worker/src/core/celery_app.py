import os
from celery import Celery

celery_app = Celery('publish_worker',
             broker=os.getenv('CELERY_BROKER_URL'),
             include=['src.tasks'])

celery_app.conf.update(
    task_queues={
        'moderation': {'exchange': 'moderation', 'routing_key': 'moderation'},
        'preview': {'exchange': 'preview', 'routing_key': 'preview'},
        'publish': {'exchange': 'publish', 'routing_key': 'publish'},
        'notifications': {'exchange': 'notifications', 'routing_key': 'notifications'},
        'dlq': {'exchange': 'dlq', 'routing_key': 'dlq'},
    },
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_time_limit=60,
    task_default_retry_delay=10,
    task_max_retries=3,
    broker_transport_options={'visibility_timeout': 3600},
)
