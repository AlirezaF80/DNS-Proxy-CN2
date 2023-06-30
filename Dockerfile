FROM python:3.9

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    redis-server

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV INPUT_PORT=53

EXPOSE $INPUT_PORT

ENV OUTPUT_PORT=53

EXPOSE $OUTPUT_PORT

CMD redis-server --bind 0.0.0.0 && python Main.py