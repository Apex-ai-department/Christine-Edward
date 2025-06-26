from fastapi import FastAPI
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

UPSTASH_REDIS_URL = os.getenv("UPSTASH_REDIS_REST_URL")  # e.g., https://<random>.upstash.io
UPSTASH_REDIS_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")

print(UPSTASH_REDIS_URL)
print(UPSTASH_REDIS_TOKEN)

app = FastAPI()

# Optional global client (used in routes)
http_client = httpx.AsyncClient()

@app.on_event("startup")
async def startup_event():
    try:
        headers = {
            "Authorization": f"Bearer {UPSTASH_REDIS_TOKEN}"
        }

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