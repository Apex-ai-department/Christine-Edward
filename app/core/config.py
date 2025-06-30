import os, httpx
from dotenv import load_dotenv

load_dotenv()

UPSTASH_REDIS_URL = os.getenv("UPSTASH_REDIS_REST_URL")
UPSTASH_REDIS_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")
headers = {
            "Authorization": f"Bearer {UPSTASH_REDIS_TOKEN}"
        }

# Optional global client (used in routes)
http_client = httpx.AsyncClient()