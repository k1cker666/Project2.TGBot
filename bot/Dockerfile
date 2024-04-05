FROM python:3-slim

WORKDIR /tgbot/

COPY *.py /tgbot/
COPY /tests/*.py /tgbot/test/
COPY /src/*.py /tgbot/src/
COPY /src/db/*.py /tgbot/src/db/
COPY /src/handlers/*.py /tgbot/src/handlers/
COPY /src/components/*.py /tgbot/src/components/
COPY /src/helpfuncs/*.py /tgbot//src/helpfuncs/

RUN apt-get update \
    && apt-get install -y redis-tools \
    && apt-get install -y postgresql-client \
    && pip install python-telegram-bot \
    && pip install psycopg[binary] \
    && pip install redis[hiredis]