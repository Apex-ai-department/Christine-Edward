# Use official Python 3.11 image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Tesseract OCR and any required dependencies
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app

# Expose port
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]