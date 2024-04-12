import redis
from redis.exceptions import ConnectionError
from loguru import logger
from src.components.config import RedisDB

def create_connectrion(config: RedisDB, decode_responses=True, charset="utf-8"):
    connection = redis.StrictRedis(
        host = config.host,
        port = config.port,
        decode_responses = decode_responses,
        charset = charset
    )
    try:
        connection.ping()
        logger.info(f'{config.host}:{config.port} - Connection to Redis DB successful')
    except ConnectionError as e:
        logger.error(f'{config.host}:{config.port} - {e}')
        logger.error('Application was not started')
        raise ConnectionError
    else: 
        return connection