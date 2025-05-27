FROM python:3.11-slim

WORKDIR /app

COPY training/ /app
COPY shared/ /app/shared

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r shared/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "train.py"]


