import redis
from redis.exceptions import ConnectionError
from loguru import logger
from src.components.config import RedisDB

def create_connectrion(config: RedisDB, decode_responses=True):
    connection = redis.Redis(
        host = config.host,
        port = config.port,
        decode_responses = decode_responses
    )
    try:
        connection.ping()
        logger.info(f'{config.host}:{config.port} - Connection to Redis DB successful')
        return connection
    except ConnectionError as e:
        logger.error(f'{config.host}:{config.port} - {e}')
        logger.error('Application was not started')
        raise ConnectionError