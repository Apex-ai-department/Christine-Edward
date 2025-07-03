from celery import Celery
from kombu import Queue
import os

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery_app = Celery("project", broker=redis_url, backend=redis_url, include=["app.workers.redisHelper"])
celery_app.autodiscover_tasks(['app.tasks'])

celery_app.conf.task_queues = (
    Queue('default', routing_key='default', queue_arguments={'x-max-priority': 255}),
)

celery_app.conf.worker_prefetch_multiplier = 1  # reduce hoarding of tasks
celery_app.conf.task_acks_late = True  # acknowledge only after processing