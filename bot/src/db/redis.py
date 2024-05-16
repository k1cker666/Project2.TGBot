import redis
from loguru import logger
from redis.exceptions import ConnectionError
from src.components.envconfig import RedisDB


def create_connection(config: RedisDB) -> redis.Redis:
    connection = redis.Redis(
        host=config.host,
        port=config.port,
        decode_responses=True,
        encoding="utf-8",
    )
    try:
        connection.ping()
        logger.info(
            f"{config.host}:{config.port} - Connection to Redis DB successful"
        )
        return connection
    except ConnectionError as e:
        logger.error(f"{config.host}:{config.port} - {e}")
        logger.info("Application was not started")
        raise ConnectionError
