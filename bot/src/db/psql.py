import psycopg_pool
import psycopg
from psycopg import OperationalError
from loguru import logger
from src.components.config import PostgresDB

def create_connection_pool(config: PostgresDB) -> psycopg_pool.ConnectionPool:
    try:
        connection = psycopg.connect(
            dbname = config.dbname,
            user = config.user,
            password = config.password,
            host = config.host,
            port = config.port
        )
    except OperationalError as e:
        logger.error(f'{config.host}:{config.port} - {e}')
        logger.info('Application was not started')
        raise OperationalError
    else:
        connection.close()
        pool = psycopg_pool.ConnectionPool(
            conninfo = f'postgresql://{config.user}:{config.password}@{config.host}:{config.port}/{config.dbname}',
            open=True,
            max_size=10
        )
        logger.info(f'{config.host}:{config.port} - Connection to PostgreSQL as user {config.user} successful')
        return pool