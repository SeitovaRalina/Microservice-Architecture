import os
from celery import Celery

celery_app = Celery(
    'dlq_worker',
    broker=os.getenv('CELERY_BROKER_URL'),
    include=['src.tasks']
)

celery_app.conf.update(
    task_queues={
        'dlq': {'exchange': 'dlq', 'routing_key': 'dlq'},
    },
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_time_limit=60,
    broker_transport_options={'visibility_timeout': 3600},
)
