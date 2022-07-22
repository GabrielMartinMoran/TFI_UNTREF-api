FROM python:3.10-buster

ARG DB_URL
ARG DB_PORT
ARG DB_USERNAME
ARG DB_PASSWORD
ARG DB_NAME
ARG PORT

ENV DB_URL = $DB_URL
ENV DB_PORT = $DB_PORT
ENV DB_USERNAME = $DB_USERNAME
ENV DB_PASSWORD = $DB_PASSWORD
ENV DB_NAME = $DB_NAME

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT python -m gunicorn -w 4 -b 0.0.0.0:$PORT src.app.api:app -c ./src/app/gunicorn_config.py