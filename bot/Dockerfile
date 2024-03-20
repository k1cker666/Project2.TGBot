FROM python:3-slim

WORKDIR /tgbot/

COPY *.py /tgbot/
COPY /tests/*.py /tgbot/test/
COPY /src/*.py /tgbot/src/
COPY /src/db/*.py /tgbot/src/db/
COPY /src/handlers/*.py /tgbot/src/handlers/

RUN apt-get update \
    && apt-get install -y redis-tools \
    && apt-get install -y postgresql-client \
    && pip install python-telegram-bot \
    && pip install psycopg2-binary \
    && pip install redis[hiredis]