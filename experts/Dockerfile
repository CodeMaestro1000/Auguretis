FROM python:3.9.7-slim

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "consumer.py"]