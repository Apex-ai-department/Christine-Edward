from fastapi import APIRouter
import os, httpx
from dotenv import load_dotenv
from app.core.config import UPSTASH_REDIS_URL, UPSTASH_REDIS_TOKEN, headers, http_client

load_dotenv()
router = APIRouter()

@router.get("/")
async def root():
    return {"message": "API is working"}

@router.get("/debug-queue") #debugger
async def debug_queue():
    response = await http_client.get(
        f"{UPSTASH_REDIS_URL}/LRANGE/receipt_jobs/0/10",  # Read first 10 jobs
        headers={"Authorization": f"Bearer {UPSTASH_REDIS_TOKEN}"}
    )
    return response.json()