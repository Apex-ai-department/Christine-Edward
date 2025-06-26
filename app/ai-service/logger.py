# ai_service/logger.py
import json
from datetime import datetime

def log_result(job_id, result):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "job_id": job_id,
        "result": result
    }
    with open("job_results.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
