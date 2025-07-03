from app.celery import celery_app
import pytesseract
from app.workers.processor import *

@celery_app.task(name='app.workers.redisHelper.process_ai_result')
def process_ai_result(result):
    # e.g. store in DB, send to another service, etc.
    print("✅ Received result in Celery:", result)

    jobID = result.get("jobId")
    urls = result.get("urls")

    #test with local images for now
    image_path = ["app/temp/0e6cfb237956bd51bd196b600-1.png"]
    imgs = [Image.open(url) for url in image_path]
    print(imgs)

    #Tesseract OCR
    #text = pytesseract.image_to_string(result)

    #OpenAI
    #parse_receipt_text(text,uploaderName)

    return True