import os, httpx
from dotenv import load_dotenv

load_dotenv()

UPSTASH_REDIS_URL = os.getenv("UPSTASH_REDIS_REST_URL")
UPSTASH_REDIS_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
headers = {
            "Authorization": f"Bearer {UPSTASH_REDIS_TOKEN}"
        }

# Optional global client (used in routes)
http_client = httpx.AsyncClient()

# Key structure (per job):
JOB_STATUS_KEY = "job:{job_id}:status"  # String type
JOB_RESULTS_KEY = "job:{job_id}:results"  # List type

# Status lifecycle:
STATUSES = [
    "queued",       # Initial state
    "preprocessing", # In batching
    "processing",    # AI working
    "completed",    # All batches done
    "failed"        # Error state
]
