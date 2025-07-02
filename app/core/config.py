import os, httpx, boto3
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# Locate project root (two levels up from config.py)
root = Path(__file__).resolve().parents[2]
dotenv_path = root / ".env"
print("Loading .env from:", dotenv_path)

# Load environment variables into os.environ
load_dotenv(dotenv_path.as_posix(), override=True)

# Now variables are accessible
UPSTASH_REDIS_URL = os.getenv("UPSTASH_REDIS_REST_URL")
UPSTASH_REDIS_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
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