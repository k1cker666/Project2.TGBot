import psycopg
from loguru import logger

try:
    connect =  psycopg.connect('postgresql://postgres:roma1234@postgres:5432/tgbot')
except psycopg.OperationalError as e:
    logger.error(f"{e}")
else:
    logger.debug("Connection is ok")
    connect.close()