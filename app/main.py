from fastapi import FastAPI, Form, Request
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

# ➕ Route to receive JSON job payload
@app.post("/submit-job")
async def submit_job(request: Request):
    data = await request.json()

    # Add timestamp and default status if not present
    job = {
        "jobId": data.get("jobId"),
        "signedURL": data.get("signedURL"),
        "uploader_name": data.get("uploader_name"),
        "createdAt": data.get("createdAt") or datetime.utcnow().isoformat(),
        "status": data.get("status", "pending")
    }

    # Push JSON string to Redis queue
    redis_resp = await http_client.post(
        f"{UPSTASH_REDIS_URL}/LPUSH/receipt_jobs/{json.dumps(job)}",
        headers=headers
    )

    return {"message": "Job queued", "job": job, "redis_response": redis_resp.json()}

# 🔁 Redis consumer
async def job_consumer():
    print("🔄 Job consumer started")
    while True:
        try:
            resp = await http_client.get(
                f"{UPSTASH_REDIS_URL}/BRPOP/receipt_jobs/5",  # block 5 sec
                headers=headers
            )
            data = resp.json()

            if isinstance(data, list) and len(data) == 2:
                _, job_json = data
                job = json.loads(job_json)
                print(f"📥 Pulled job: {job['jobId']} from {job['uploader_name']}")

                # Download image from signedURL
                img_resp = await http_client.get(job["signedURL"])
                img_resp.raise_for_status()

                image = Image.open(BytesIO(img_resp.content))
                print(f"✅ Processed image {job['jobId']} — size: {image.size}")

                # Optional: update status, save, or pass to OCR

            else:
                await asyncio.sleep(1)

        except Exception as e:
            print("❌ Error in consumer:", e)
            await asyncio.sleep(2)


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

    except Exception as e:
        print("❌ Failed to connect to Upstash Redis:", e)