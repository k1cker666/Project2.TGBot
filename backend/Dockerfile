FROM python:3-slim

WORKDIR /project/

COPY *.py /project/backend/
COPY requirements.txt /project/backend/

RUN apt-get update \
    && apt-get install -y postgresql-client \
    && pip install -r /project/backend/requirements.txt

CMD [ "python", "/project/backend/main.py" ]