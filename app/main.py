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

load_dotenv()

UPSTASH_REDIS_URL = os.getenv("UPSTASH_REDIS_REST_URL")  # e.g., https://<random>.upstash.io
UPSTASH_REDIS_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")

headers = {
            "Authorization": f"Bearer {UPSTASH_REDIS_TOKEN}"
        }

app = FastAPI()

# Optional global client (used in routes)
http_client = httpx.AsyncClient()

#loop through redis queue
async def fetch_from_redis():
    print("🚀 Starting to consume URLs from Redis queue...")
    while True:
        try:
            # Call BRPOP (blocking pop for 5 seconds)
            resp = await http_client.get(
                f"{UPSTASH_REDIS_URL}/LPOP/receipt_jobs/5",
                headers=headers
            )

            print("📦 Raw LPOP response:", resp.text)

            result = resp.json().get("result")

            if result and isinstance(result, list) and len(result) == 2:
                _, job_json = result

                print("🧾 Job JSON string:", job_json)

                try:
                    job = json.loads(job_json)
                    url = job.get("signedURL")

                    if url:
                        print(f"✅ Pulled URL: {url}")
                        yield url
                    else:
                        print("⚠️ Job missing 'signedURL':", job)

                except json.JSONDecodeError as json_err:
                    print("❌ JSON decode error:", json_err, "| Raw:", job_json)

            else:
                print("⏳ No job found, sleeping...")
                await asyncio.sleep(1)

        except Exception as e:
            print("❌ Exception in fetch loop:", e)
            await asyncio.sleep(2)

async def print_urls_from_redis():
    async for url in fetch_from_redis():
        print(f"🖨️ URL from Redis: {url}")

#download images from AWS
async def download_image(url: str) -> Image.Image:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()  # Raise if not 200 OK
        img = Image.open(BytesIO(response.content))
        return img

@app.get("/debug-queue") #debugger
async def debug_queue():
    response = await http_client.get(
        f"{UPSTASH_REDIS_URL}/LRANGE/receipt_jobs/0/10",  # Read first 10 jobs
        headers={"Authorization": f"Bearer {UPSTASH_REDIS_TOKEN}"}
    )
    return response.json()

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
        asyncio.create_task(print_urls_from_redis())

    except Exception as e:
        print("❌ Failed to connect to Upstash Redis:", e)

@app.get("/")
async def root():
    return {"message": "API is working"}
