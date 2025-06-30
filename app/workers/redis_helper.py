from PIL import Image
import json
import httpx
from io import BytesIO
import asyncio
from app.core.config import UPSTASH_REDIS_URL, UPSTASH_REDIS_TOKEN, headers, http_client

#loop through redis queue
async def fetch_from_redis(http_client, UPSTASH_REDIS_URL, headers):
    print("🚀 Starting to consume URLs from Redis queue...")
    while True:
        try:
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