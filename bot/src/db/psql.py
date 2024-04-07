import psycopg
from psycopg import OperationalError
import logging

def create_connection(db_name='tgbot', db_user='postgres', db_password='roma1234', db_host='localhost', db_port='5432'): # db_host='localhost'/'postgres'
    logger = logging.getLogger(__name__)
    connection = None
    try:
        connection = psycopg.connect(
            dbname = db_name,
            user = db_user,
            password = db_password,
            host = db_host,
            port = db_port,
            autocommit = True
        )
        logger.info(f'{db_host}:{db_port} - Connection to PostgreSQL as user {db_user} successful')
        return connection
    except OperationalError as e:
        logger.error(f'{e}')
        logger.info('Application was not started')
        raise OperationalError