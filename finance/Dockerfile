FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 50051

ENV REDIS_HOST localhost
ENV REDIS_PORT 6379

CMD python3 app.py
