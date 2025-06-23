#sets image to python
FROM python:3.11

# /app as default folder
WORKDIR /app

# copy dependency file (requirements.txt) into container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copies files into container like main.py
COPY . .

# Run FastAPI from main.app from main.py on startup
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
