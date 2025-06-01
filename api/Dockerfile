FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

COPY /api /app/api
COPY /shared /app/shared

RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r api/requirements.txt
RUN pip install -r api/requirements.txt
# RUN pip install --no-cache-dir -r shared/requirements.txt
RUN pip install -r shared/requirements.txt

# Expose port (optional)
EXPOSE 8000

# Start FastAPI server
# CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
