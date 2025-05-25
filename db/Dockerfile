FROM python:3.11-slim

WORKDIR /app

COPY db/ /app
COPY shared/ /app/shared
COPY .env /app/.env

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r shared/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "init.py"]
