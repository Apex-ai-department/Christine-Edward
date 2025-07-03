from fastapi import FastAPI, Form, Request
from pydantic import BaseModel
import httpx
import os
import asyncio
import json
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
from datetime import datetime
from app.workers.redisHelper import *
from app.routers.debug import router as debug_router
from app.core.config import *
from pathlib import Path
from app.tasks import *
from app.workers.awsHelper import *


load_dotenv()

app = FastAPI()
app.include_router(debug_router)

@app.on_event("startup")
async def startup_event():
    try:
        # Example: SET key = "hello"
        set_resp = await http_client.post(
            f"{UPSTASH_REDIS_URL}/SET/mykey/hello",
            headers=headers
        )

        # Example: GET key
        get_resp = await http_client.get(
            f"{UPSTASH_REDIS_URL}/GET/mykey",
            headers=headers
        )

        print("✅ Connected to Upstash Redis. Value:", get_resp.json())

        #access redis queue
        asyncio.create_task(consume_loop())

    except Exception as e:
        print("❌ Failed to connect to Upstash Redis:", e)

async def consume_loop():
    async for job in fetch_from_redis(http_client, UPSTASH_REDIS_URL, headers):
        #for testing the AWS
        # print(job)
        # awsLink = job.get("urls")
        # download_image_from_s3(awsLink[0])

        # print("urls:", job.get("urls"))
        print("uploaderName:", job["metadata"]["uploaderName"])
        
        async for aiJob in aiBatcher(job["jobID"], job["urls"], job["metadata"]["uploaderName"], 5):
            # process each result here
            print("Got result:", aiJob)

            # Send to Celery for background processing
            length = aiJob["batchSize"]
            priority = max(0, 255 - length)

            #pushing test job
            print("Sending task to Celery with aiJob:", aiJob)
            res = process_ai_result.apply_async(args=[aiJob], queue='default', priority=priority)

            print("Task ID:", res.id)
            print("Status:", res.status)