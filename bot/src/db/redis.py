import redis
from redis.exceptions import ConnectionError
from loguru import logger
from src.components.config import RedisDB

def create_connection(config: RedisDB):
    connection = redis.Redis(
        host = config.host,
        port = config.port,
        decode_responses = True,
        charset = "utf-8"
    )
    try:
        connection.ping()
        logger.info(f'{config.host}:{config.port} - Connection to Redis DB successful')
    except ConnectionError as e:
        logger.error(f'{config.host}:{config.port} - {e}')
        logger.info('Application was not started')
        raise ConnectionError
    else: 
        return connection