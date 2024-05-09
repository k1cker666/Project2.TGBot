FROM python:3-slim

WORKDIR /project/

COPY /scripts/*.py /project/bot/scripts/
COPY /scripts/requirements.txt /project/bot/scripts/
COPY /scripts/sql/insert_word_dataset.sql /project/bot/scripts/sql
COPY /migrations/*.sql /project/bot/migrations/
COPY /config/*.json /project/bot/config/

RUN apt-get update \
    && apt-get install -y postgresql-client \
    && pip install -r /project/bot/scripts/requirements.txt