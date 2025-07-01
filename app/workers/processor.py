from PIL import Image
import pytesseract
import requests
from io import BytesIO
import json
import os
from openai import OpenAI


def ocr_processing(image,uploaderName):
    try:
        raw_text = pytesseract.image_to_string(image, lang = "jpn")

        # Step 4: Structure the data (simplified example)
        structured_data = parse_receipt_text(raw_text,uploaderName)

        return {
            "raw_text": raw_text,
            "structured": structured_data
        }
    except Exception as e:
        print("OCR Failed: {e}")
        return None


def parse_receipt_text(text,uploaderName): #OPENAI DONE HERE
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
    Prefer japanese language over english, only use english if it is indicated, do not try to translate to english.
    Analyze this receipt and respond with ONLY a JSON object in this exact format:
    {{
        "uploader_name": "{uploaderName}",
        "receipt_type": "decide whether it is a 'grocery' or 'internet telephone payment' or 'parking' or whatever is the best category you can decide dont forget in japanese langauge also",
        "date": "date of purchase",
        "company_name": "the company name on the receipt",
        "price": "the full amount paid in Japanese yen, no unit",
    }}
    OCRテキスト:
    {text}
    """

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        # Extract and parse JSON
        json_text = response.choices[0].message.content
        receipt_json = json.loads(json_text)
        return receipt_json

    except json.JSONDecodeError:
        raise ValueError("GPT parsing failed", json_text)
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")

    # Mock OCR and OpenAI
    # text = f"Mock text from {image_url}"
    # formatted_data = {
    #    "total": round(random.uniform(1.0, 100.0), 2),
    #    "merchant": f"Merchant_{random.randint(1, 100)}"
    # }
    # return formatted_data
