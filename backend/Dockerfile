FROM python:3.10-slim

WORKDIR /project/

COPY /backend/*.py /project/backend/
COPY poetry.lock /project/
COPY pyproject.toml /project/

RUN apt-get update \
    && apt-get install -y postgresql-client \
    && pip install poetry \
    && pip install --upgrade pip \
    && poetry config virtualenvs.create false \
    && poetry install --only backend --no-root

CMD [ "python", "/project/backend/main.py" ]