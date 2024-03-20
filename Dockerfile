FROM python:3-slim

WORKDIR /tgbot

COPY /bot /tgbot

RUN pip install -U pip
RUN pip install python-telegram-bot
RUN pip install psycopg2-binary
RUN pip install redis[hiredis]
RUN docker-compose -f ./bot/src/db/docker-compose.yml up

CMD [ "python3", "main.py" ]