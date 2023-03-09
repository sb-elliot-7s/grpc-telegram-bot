FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV PORT 8001
ENV HOST 0.0.0.0

CMD uvicorn app:app --host $HOST --port $PORT --reload
