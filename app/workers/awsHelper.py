from PIL import Image
from urllib.parse import urlparse
from io import BytesIO
from app.celery import celery_app
from app.core.config import *
from app.workers.awsHelper import *
import boto3

def download_image_from_s3(s3_url: str):
    # Remove the 's3://' prefix
    path = s3_url[5:]
    # Split once at the first slash to separate bucket and key
    bucket_name, object_key = path.split('/', 1)

    # Initialize S3 client with credentials and region
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION
    )

    # Fetch the object from S3
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    data = response['Body'].read()

    # Load image from bytes
    image = Image.open(BytesIO(data))
    print("Download success")
    return image