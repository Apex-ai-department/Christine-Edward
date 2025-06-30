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
from app.workers.redis_helper import fetch_from_redis, download_image, print_urls_from_redis
from app.routers.debug import router as debug_router
from app.core.config import UPSTASH_REDIS_URL, UPSTASH_REDIS_TOKEN, headers, http_client



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
    fetch_from_redis(http_client, UPSTASH_REDIS_URL, headers)

#debugging/status check
'''@app.get("/")
async def root():
    return {"message": "API is working"}

@app.get("/debug-queue") #debugger
async def debug_queue():
    response = await http_client.get(
        f"{UPSTASH_REDIS_URL}/LRANGE/receipt_jobs/0/10",  # Read first 10 jobs
        headers={"Authorization": f"Bearer {UPSTASH_REDIS_TOKEN}"}
    )
    return response.json()'''
