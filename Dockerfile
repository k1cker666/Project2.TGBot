FROM python:3-slim

WORKDIR /tgbot

COPY /bot /tgbot

RUN pip install python-telegram-bot

CMD [ "python3", "main.py" ]