# ai_service/worker.py
import json
import time
from redis_client import redis_client

QUEUE_NAME = "image_jobs"

def process_job(job_data):
    """Mock image processing logic"""
    print(f"Processing job: {job_data['job_id']}")
    time.sleep(1)  # Simulate OCR/OpenAI processing
    return {"status": "completed", "result": "mock_text"}

def consume_jobs():
    while True:
        try:
            # Blocking pop (waits indefinitely for jobs)
            _, job_json = redis_client.blpop(QUEUE_NAME, timeout=30)
            job_data = json.loads(job_json)
            
            # Process job
            result = process_job(job_data)
            
            # Log result
            with open("job_results.log", "a") as f:
                f.write(f"{job_data['job_id']}: {result}\n")
            
        except Exception as e:
            print(f"Error processing job: {e}")

if __name__ == "__main__":
    consume_jobs()
