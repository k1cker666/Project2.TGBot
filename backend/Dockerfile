FROM python:3.10-slim as builder

ENV POETRY_VERSION=1.8.3 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

RUN apt update \
    && apt install -y \
    postgresql-client \
    redis-tools \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir poetry==${POETRY_VERSION} \
    && pip install --upgrade --no-cache-dir pip \
    && poetry config virtualenvs.create false 

WORKDIR /project/

COPY poetry.lock pyproject.toml .env /project/
RUN poetry install --only=backend --no-root --no-directory

COPY /backend/*.py /project/backend/
COPY /backend/static/*.html /project/backend/static/
COPY /backend/static/images/*.png /project/backend/static/images/
COPY /backend/src/*.py /project/backend/src/
COPY /backend/src/components/*.py /project/backend/src/components/

WORKDIR /project/backend/