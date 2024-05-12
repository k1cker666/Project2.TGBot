FROM python:3.10-slim

ENV POETRY_VERSION=1.8.3 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

RUN apt update \
    && apt install -y \
    redis-tools \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir poetry==${POETRY_VERSION} \
    && pip install --upgrade --no-cache-dir pip \
    && poetry config virtualenvs.create false 

WORKDIR /project/

COPY poetry.lock pyproject.toml /project/
RUN poetry install --only tgbot --no-root --no-directory

COPY .env /project/
COPY /bot/*.py /project/bot/
COPY /bot/tests/*.py /project/bot/test/
COPY /bot/src/*.py /project/bot/src/
COPY /bot/src/db/*.py /project/bot/src/db/
COPY /bot/src/handlers/*.py /project/bot/src/handlers/
COPY /bot/src/components/*.py /project/bot/src/components/
COPY /bot/src/helpfuncs/*.py /project/bot/src/helpfuncs/
COPY /bot/src/models/*.py /project/bot/src/models/
COPY /bot/src/repository/*.py /project/bot/src/repository/
COPY /bot/images/*template.png /project/bot/images/
COPY /bot/fonts/*.ttf /project/bot/fonts/