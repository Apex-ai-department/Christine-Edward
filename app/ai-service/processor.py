# ai_service/processor.py
import random

def mock_ocr_processing(image_url):
    """Simulate Tesseract + OpenAI processing"""
    # Mock "download" from S3
    print(f"Downloading {image_url}...")
    
    # Mock OCR and OpenAI
    text = f"Mock text from {image_url}"
    formatted_data = {
        "total": round(random.uniform(1.0, 100.0), 2),
        "merchant": f"Merchant_{random.randint(1, 100)}"
    }
    return formatted_data
