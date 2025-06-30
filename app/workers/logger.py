import json
from datetime import datetime

def log_result(jobId, batchId, imgType):
    '''log_entry = {
        "timestamp": datetime.now().isoformat(),
        "job_id": job_id,
        "result": result
    }'''

    log_entry = {
        "jobId": jobId,
        "batchId": batchId,
        "type": imgType,
        "files": [
            {
            "s3Key": "uploads/batch_abc123def456/xyz789_receipt1.jpg",
            "s3Url": "https://my-bucket.s3.amazonaws.com/uploads/batch_abc123def456/xyz789_receipt1.jpg",
            "originalName": "receipt1.jpg"
            },
            {
            "s3Key": "uploads/batch_abc123def456/abc456_receipt2.jpg",
            "s3Url": "https://my-bucket.s3.amazonaws.com/uploads/batch_abc123def456/abc456_receipt2.jpg",
            "originalName": "receipt2.jpg"
            }
        ],
        "metadata": {
            "uploaderName": "John Doe",
            "uploadedAt": "2025-06-30T10:30:00.000Z",
            "totalFiles": 2,
            "successfulFiles": 2
        },
        "createdAt": "2025-06-30T10:30:15.000Z",
        "status": "pending"
        }
    
    with open("job_results.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n")