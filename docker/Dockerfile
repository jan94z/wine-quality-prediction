FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Install Python dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app and models
COPY ./app /app/app
COPY ./training/models /app/models

# Optionally copy .env file if needed
# COPY .env /app/.env

# Expose port (optional)
EXPOSE 80

# Define healthcheck (optional)
#HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
 # CMD curl --fail http://localhost/health || exit 1

# Start FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
