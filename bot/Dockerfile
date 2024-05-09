FROM python:3-slim

WORKDIR /project/

COPY *.py /project/bot/
COPY requirements.txt /project/bot/
COPY /tests/*.py /project/bot/test/
COPY /src/*.py /project/bot/src/
COPY /src/db/*.py /project/bot/src/db/
COPY /src/handlers/*.py /project/bot/src/handlers/
COPY /src/components/*.py /project/bot/src/components/
COPY /src/helpfuncs/*.py /project/bot/src/helpfuncs/
COPY /src/models/*.py /project/bot/src/models/
COPY /src/repository/*.py /project/bot/src/repository/
COPY /config/*.json /project/bot/config/
COPY /images/*template.png /project/bot/images/
COPY /fonts/*.ttf /project/bot/fonts/

RUN apt-get update \
    && apt-get install -y redis-tools \
    && apt-get install -y postgresql-client \
    && pip install -r /project/bot/requirements.txt