FROM python:3.10-slim

WORKDIR /project/

COPY /bot/scripts/*.py /project/bot/scripts/
COPY /bot/scripts/sql/insert_word_dataset.sql /project/bot/scripts/sql
COPY /bot/migrations/*.sql /project/bot/migrations/
COPY /bot/config/*.json /project/bot/config/
COPY poetry.lock /project/
COPY pyproject.toml /project/

RUN apt-get update \
    && apt-get install -y postgresql-client \
    && pip install poetry \
    && pip install --upgrade pip \
    && poetry config virtualenvs.create false \
    && poetry install --only migrations --no-root