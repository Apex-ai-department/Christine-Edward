from PIL import Image
from urllib.parse import urlparse
import json
import httpx
from io import BytesIO
import asyncio
from app.celery import celery_app
from app.core.config import *
from app.workers.awsHelper import *


#loop through redis queue
async def fetch_from_redis(http_client, UPSTASH_REDIS_URL, headers):
    print("🚀 Starting to consume URLs from Redis queue...")
    while True:
        try:
            resp = await http_client.get(
                f"{UPSTASH_REDIS_URL}/LPOP/receipt_jobs/5",
                headers=headers
            )
            result = resp.json().get("result")

            if result and len(result) > 0:
                job_json = result[0]  # get the string
                job = json.loads(job_json)

                try:
                    #extract data from web service jobs
                    job = json.loads(job_json)
                    jobId = job.get("jobId")
                    urls = [file.get("s3Url") for file in job.get("files")]
                    
                    results = {"jobID": jobId,
                               "urls": urls}
                    
                    yield results

                except json.JSONDecodeError as json_err:
                    print("❌ JSON decode error:", json_err, "| Raw:", job_json)

            else:
                print("⏳ No job found, sleeping...")
                await asyncio.sleep(1)

        except Exception as e:
            print("❌ Exception in fetch loop:", e)
            await asyncio.sleep(2)

async def aiBatcher(jobID, urls, batchSize):
    while urls:
        urlList = []
        for i in range(batchSize): 
            if urls:
                urlList.append(urls.pop())
        aiJob = {"jobID": jobID, "urlBatch": urlList, "batchSize": len(urlList)}
        yield aiJob


    