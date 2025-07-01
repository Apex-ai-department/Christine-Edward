import pytest
from PIL import Image
from io import BytesIO
from your_module import download_image  # adjust import path
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

@pytest.mark.asyncio
async def test_download_image_success():
    url = "https://httpbin.org/image/png"
    img = await download_image(url)
    assert isinstance(img, Image.Image)
    assert img.format == "PNG"
    assert img.size[0] > 0 and img.size[1] > 0