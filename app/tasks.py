from app.celery import celery_app

@celery_app.task(name='app.workers.redisHelper.process_ai_result')
def process_ai_result(result):
    # e.g. store in DB, send to another service, etc.
    print("✅ Received result in Celery:", result)
    return True