FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV PORT 8000
ENV HOST 0.0.0.0

CMD uvicorn main:app --reload --host $HOST --port $PORT