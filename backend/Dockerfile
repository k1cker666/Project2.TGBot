FROM python:3.10-slim as builder

ENV POETRY_VERSION=1.8.3 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

RUN apt update \
    && apt install -y postgresql-client \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir poetry==${POETRY_VERSION} \
    && pip install --upgrade --no-cache-dir pip \
    && poetry config virtualenvs.create false 

WORKDIR /project/

COPY poetry.lock pyproject.toml /project/
RUN poetry install --only backend --no-root --no-directory

COPY /backend/*.py /project/backend/
COPY .env /project/

CMD [ "python", "/project/backend/main.py" ]