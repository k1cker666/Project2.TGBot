import psycopg
from psycopg import OperationalError
from loguru import logger
from src.components.config import PostgresDB

def create_connection(config: PostgresDB) -> psycopg.Connection:
    connection = None
    try:
        connection = psycopg.connect(
            dbname = config.dbname,
            user = config.user,
            password = config.password,
            host = config.host,
            port = config.port,
            autocommit = True
        )
        logger.info(f'{config.host}:{config.port} - Connection to PostgreSQL as user {config.user} successful')
        return connection
    except OperationalError as e:
        logger.error(f'{config.host}:{config.port} - {e}')
        logger.error('Application was not started')
        raise OperationalError