# Base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy dependency list first (to cache layers)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Run FastAPI on startup
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
