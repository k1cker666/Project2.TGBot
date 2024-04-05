FROM python:3-slim

WORKDIR /project/

COPY /scripts/*.py /project/bot/scripts/
COPY /migrations/*.sql /project/bot/migrations/

RUN apt-get update \
    && apt-get install -y postgresql-client \
    && pip install psycopg[binary]