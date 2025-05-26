FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

COPY /api /app/
COPY /shared /app/shared
COPY .env /app/.env

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r shared/requirements.txt

# Expose port (optional)
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
