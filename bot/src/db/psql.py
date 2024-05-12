import psycopg_pool
from loguru import logger
from psycopg import OperationalError
from src.components.config import PostgresDB


def create_connection_pool(config: PostgresDB) -> psycopg_pool.ConnectionPool:
    pool = psycopg_pool.ConnectionPool(
        conninfo=f"postgresql://{config.user}:{config.password}@{config.host}:{config.port}/{config.dbname}",
        open=True,
        max_size=config.pool_max_size,
    )
    try:
        conn = pool.getconn()
    except OperationalError as e:
        logger.error(f"{config.host}:{config.port} - {e}")
        logger.info("Application was not started")
        raise OperationalError
    else:
        pool.putconn(conn)
        logger.info(
            f"{config.host}:{config.port} - Connection to PostgreSQL as user {config.user} successful"
        )
        return pool
