FROM python:3.10-slim

ENV POETRY_VERSION=1.8.3 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

RUN apt update \
    && apt install -y postgresql-client \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir poetry==${POETRY_VERSION} \
    && pip install --upgrade --no-cache-dir pip \
    && poetry config virtualenvs.create false 

WORKDIR /project/

COPY poetry.lock pyproject.toml .env /project/
RUN poetry install --only=migrations --no-root --no-directory

COPY /bot/scripts/run_migrations.py /project/bot/scripts/
COPY /bot/scripts/run_sql.py /project/bot/scripts/
COPY /bot/scripts/main.py /project/bot/scripts/
COPY /bot/scripts/sql/insert_word_dataset.sql /project/bot/scripts/sql
COPY /bot/migrations/*.sql /project/bot/migrations/
