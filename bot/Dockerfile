FROM python:3.10-slim

WORKDIR /project/

COPY /bot/*.py /project/bot/
COPY /bot/tests/*.py /project/bot/test/
COPY /bot/src/*.py /project/bot/src/
COPY /bot/src/db/*.py /project/bot/src/db/
COPY /bot/src/handlers/*.py /project/bot/src/handlers/
COPY /bot/src/components/*.py /project/bot/src/components/
COPY /bot/src/helpfuncs/*.py /project/bot/src/helpfuncs/
COPY /bot/src/models/*.py /project/bot/src/models/
COPY /bot/src/repository/*.py /project/bot/src/repository/
COPY /bot/config/*.json /project/bot/config/
COPY /bot/images/*template.png /project/bot/images/
COPY /bot/fonts/*.ttf /project/bot/fonts/
COPY poetry.lock /project/
COPY pyproject.toml /project/

RUN apt-get update \
    && apt-get install -y redis-tools \
    && apt-get install -y postgresql-client \
    && pip install poetry \
    && pip install --upgrade pip \
    && poetry config virtualenvs.create false \
    && poetry install --only tgbot --no-root