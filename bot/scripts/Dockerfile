FROM python:3-slim

WORKDIR /tgbot/

COPY *.py /tgbot/scripts/
COPY /migrations/*.sql /tgbot/bot/scripts/migrations/

RUN apt-get update \
    && apt-get install -y postgresql-client \
    && pip install psycopg[binary]