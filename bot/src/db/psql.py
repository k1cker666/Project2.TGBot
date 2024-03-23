import psycopg2
from psycopg2 import OperationalError
import logging

def create_connection(db_name='postgres', db_user='postgres', db_password='roma1234', db_host='postgres', db_port='5432'):
    logger = logging.getLogger(__name__)
    connection = None
    try:
        connection = psycopg2.connect(
            database = db_name,
            user = db_user,
            password = db_password,
            host = db_host,
            port = db_port
        )
        logger.info('Connection to PostgreSQL DB successful')
    except OperationalError as e:
        logger.info(f'{e}')