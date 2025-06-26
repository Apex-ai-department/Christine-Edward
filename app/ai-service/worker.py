# ai_service/worker.py
import json
import time
from redis_client import redis_client

QUEUE_NAME = "jobs"

def process_job(job_data):
    """Mock image processing logic"""
    print(f"Processing job: {job_data['job_id']}")
    time.sleep(1)  # Simulate OCR/OpenAI processing
    return {"status": "completed", "result": "mock_text"}

def consume_jobs():
    while True:
        try:
            # Blocking pop (waits indefinitely for jobs)
            job_data = redis_client.blpop("jobs", timeout=30)  # Wait 30 sec max
            if job_data is None:
                print("No jobs in queue. Waiting...")
                continue
            # Process job
            _, job_json = job_data  # Unpack only if job exists
            job = json.loads(job_json)

            result = process_job(job_data)
            print(f"Processed: {result}")

            # Log result
            #with open("job_results.log", "a") as f:
                #f.write(f"{job_data['job_id']}: {result}\n")
            
        except Exception as e:
            print(f"Error processing job: {e}")

if __name__ == "__main__":
    consume_jobs()
