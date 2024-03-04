FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY server.py /app/server.py

