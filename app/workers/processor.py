from PIL import Image
import pytesseract
import requests
from io import BytesIO
import json
import os
import random


def ocr_processing(image):
    # Mock "download" from S3
    try:
        raw_text = pytesseract.image_to_string(image)

        # Step 4: Structure the data (simplified example)
        structured_data = parse_receipt_text(raw_text)

        return {
            "raw_text": raw_text,
            "structured": structured_data
        }
    except Exception as e:
        print("OCR Failed: {e}")
        return None


def parse_receipt_text(text):
    lines = text.split('\n')
    merchant = lines[0] if lines else "UNKNOWN"

    # Find total (crude example)
    total = None
    for line in lines:
        if "total" in line.lower():
            total = float(''.join(c for c in line if c.isdigit() or c == '.'))

    return {
        "merchant": merchant,
        "total": total or 0.0
    }

    # Mock OCR and OpenAI
    # text = f"Mock text from {image_url}"
    # formatted_data = {
    #    "total": round(random.uniform(1.0, 100.0), 2),
    #    "merchant": f"Merchant_{random.randint(1, 100)}"
    # }
    # return formatted_data
