from PIL import Image
from urllib.parse import urlparse
import json
import httpx
from io import BytesIO
import asyncio
from app.celery import celery_app
from app.core.config import *
from app.workers.awsHelper import *
from openai import OpenAI



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
                    metadata = job.get("metadata")
                    
                    results = {"jobID": jobId,
                               "urls": urls,
                               "metadata": metadata}
                    
                    yield results

                except json.JSONDecodeError as json_err:
                    print("❌ JSON decode error:", json_err, "| Raw:", job_json)

            else:
                print("⏳ No job found, sleeping...")
                await asyncio.sleep(1)

        except Exception as e:
            print("❌ Exception in fetch loop:", e)
            await asyncio.sleep(2)

async def aiBatcher(jobID, urls, uploaderName, batchSize):
    while urls:
        urlList = []
        for i in range(batchSize): 
            if urls:
                urlList.append(urls.pop())
        aiJob = {"jobID": jobID, "urlBatch": urlList, "batchSize": len(urlList), "uploaderName": uploaderName}
        yield aiJob

async def openAI(text, uploaderName):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    completion = client.chat.completions.create(
        model="gpt-4o-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello."}
        ]
    )

    print(completion.choices[0].message)

    # prompt = f"""
    # Prefer japanese language over english, only use english if it is indicated, do not try to translate to english.
    # Analyze this receipt and respond with ONLY a JSON object in this exact format:
    # {{
    #     "uploader_name": "{uploaderName}",
    #     "receipt_type": "decide whether it is a 'grocery' or 'internet telephone payment' or 'parking' or whatever is the best category you can decide dont forget in japanese langauge also",
    #     "date": "date of purchase",
    #     "company_name": "the company name on the receipt",
    #     "price": "the full amount paid in Japanese yen, no unit",
    # }}
    # OCRテキスト:
    # {text}
    # """

    # try:
    #     # Call OpenAI API
    #     response = client.chat.completions.create(
    #         model="gpt-3.5-turbo",
    #         messages=[{"role": "user", "content": prompt}],
    #         temperature=0
    #     )

    #     # Extract and parse JSON
    #     json_text = response.choices[0].message.content
    #     receipt_json = json.loads(json_text)
    #     return receipt_json

    # except json.JSONDecodeError:
    #     raise ValueError("GPT parsing failed", json_text)
    # except Exception as e:
    #     raise Exception(f"OpenAI API error: {str(e)}")


    