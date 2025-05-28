
FROM python:3.11-slim

RUN pip install --upgrade pip
RUN pip install mlflow
RUN pip install psycopg2-binary
RUN pip install click

WORKDIR /app

COPY ci/promotion/ /app

ENTRYPOINT ["python", "promote.py"]