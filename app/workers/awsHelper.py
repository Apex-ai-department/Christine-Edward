from PIL import Image
from urllib.parse import urlparse
import json
import httpx
from io import BytesIO
import asyncio
from app.celery import celery_app
from app.core.config import *
from app.workers.awsHelper import *
import boto3

def download_image_from_s3(url):
    parsed_url = urlparse(url)
    bucket_name = parsed_url.netloc.split('.')[0]
    object_key = parsed_url.path.lstrip('/')

    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    data = response['Body'].read()  # Read the bytes

    # Load image bytes into PIL Image
    image = Image.open(BytesIO(data))
    print("download success")
    return image