import pytest
from PIL import Image
from io import BytesIO
import redis
from fastapi import APIRouter
import os, httpx
from dotenv import load_dotenv
from app.core.config import *
from app.tasks import *
from app.workers.redisHelper import *
from app.workers.awsHelper import *

load_dotenv()
router = APIRouter()

@router.get("/")
async def root():
    return {"message": "API is working"}

@router.get("/debug-queue") #debugger
async def debug_queue():
    response = await http_client.get(
        f"{UPSTASH_REDIS_URL}/LRANGE/receipt_jobs/0/10",  # Read first 10 jobs
        headers={"Authorization": f"Bearer {UPSTASH_REDIS_TOKEN}"}
    )
    return response.json()

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

@router.get("/debug-celery-queue")
async def debug_celery_queue():
    queue_name = "celery"
    length = r.llen(queue_name)
    tasks = r.lrange(queue_name, 0, 4)  # First 5 tasks
    decoded_tasks = []
    for task in tasks:
        try:
            decoded_tasks.append(json.loads(task))
        except Exception as e:
            decoded_tasks.append({"raw": task, "error": str(e)})
    return {"length": length, "tasks": decoded_tasks}

@router.get("/send-test-task")
async def send_test_task():
    result = process_ai_result.delay({"hello": "world"})
    return {"task_id": result.id}

@pytest.mark.asyncio
async def test_download_image_success():
    url = "https://httpbin.org/image/png"
    img = await download_from_s3_url(url)
    assert isinstance(img, Image.Image)
    assert img.format == "PNG"
    assert img.size[0] > 0 and img.size[1] > 0

@router.get("/jobs/{job_id}/status")
async def get_job_status(job_id: str):
    return {
        "status": r.get(f"job:{job_id}:status"),
        "results": r.lrange(f"job:{job_id}:results", 0, -1)
    }


