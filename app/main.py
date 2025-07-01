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
        async for result in aiBatcher(job["jobID"], job["urls"], 5):
            # process each result here
            print("Got result:", result)

            # Send to Celery for background processing
            res = process_ai_result.delay(result)
            print("Task ID:", res.id)
            print("Status:", res.status)

