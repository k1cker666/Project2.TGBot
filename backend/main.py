import os

import psycopg
from dotenv import load_dotenv
from loguru import logger


load_dotenv()

db_name = os.getenv("PSQL_DBNAME")
db_user = os.getenv("PSQL_USER")
db_password = os.getenv("PSQL_PASSWORD")
db_host = os.getenv("PSQL_HOST")
db_port = os.getenv("PSQL_PORT")

try:
    connect = psycopg.connect(
        f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
except psycopg.OperationalError as e:
    logger.error(f"{e}")
else:
    logger.debug("Connection is ok")
    connect.close()
