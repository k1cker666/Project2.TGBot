import psycopg_pool
from loguru import logger
from psycopg import OperationalError
from src.components.envconfig import PostgreSQLConfig


class PostgreSQL:

    connection_pool: psycopg_pool.ConnectionPool
    config: PostgreSQLConfig

    def __init__(self, config: PostgreSQLConfig):
        self.config = config
        self.__create_pool()

    def __create_pool(self):
        self.connection_pool = psycopg_pool.ConnectionPool(
            conninfo=self.config.get_conninfo(),
            open=True,
            max_size=self.config.pool_max_size,
        )
        try:
            conn = self.connection_pool.getconn()
        except OperationalError as e:
            logger.error(f"{self.config.host}:{self.config.port} - {e}")
            logger.info("Application was not started")
            raise OperationalError
        else:
            self.connection_pool.putconn(conn)
            logger.info(
                f"{self.config.host}:{self.config.port} - Connection to PostgreSQL as user {self.config.user} successful"
            )
