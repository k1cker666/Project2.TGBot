FROM python:3-slim

WORKDIR /project/

COPY *.py /project/bot/
COPY /tests/*.py /project/bot/test/
COPY /src/*.py /project/bot/src/
COPY /src/db/*.py /project/bot/src/db/
COPY /src/handlers/*.py /project/bot/src/handlers/
COPY /src/components/*.py /project/bot/src/components/
COPY /src/helpfuncs/*.py /project/bot/src/helpfuncs/

RUN apt-get update \
    && apt-get install -y redis-tools \
    && apt-get install -y postgresql-client \
    && pip install python-telegram-bot \
    && pip install psycopg[binary] \
    && pip install redis[hiredis]