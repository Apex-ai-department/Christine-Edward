from app.celery import celery_app
import pytesseract
from app.workers.processor import *

@celery_app.task(name='app.tasks.process_ai_result')
def process_ai_result(result):
    # e.g. store in DB, send to another service, etc.
    print("✅ Received result in Celery:", result)

    jobID = result.get("jobId")
    urls = result.get("urls")

    #test with local images for now
    image_path = ["app/temp/0e6cfb237956bd51bd196b600-1.png"]
    imgList = [Image.open(url) for url in image_path]
    print("Images in Celery:", imgList)

    #Tesseract OCR
    print("Sending img to OCR...")
    text = [pytesseract.image_to_string(img) for img in imgList]
    print("OCR Result:", text)

    #OpenAI
    #parse_receipt_text(text,uploaderName)

    return True