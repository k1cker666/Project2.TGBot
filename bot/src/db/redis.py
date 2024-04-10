import redis
from redis.exceptions import ConnectionError
from loguru import logger

def create_connectrion(db_host='localhost', db_port=6379, decode_responses=True): # db_host='localhost'/'redis'
    connection = redis.Redis(
        host = db_host,
        port = db_port,
        decode_responses = decode_responses
    )
    try:
        connection.ping()
        logger.info(f'{db_host}:{db_port} - Connection to Redis DB successful')
        return connection
    except ConnectionError as e:
        logger.error(f'{db_host}:{db_port} - {e}')
        logger.info('Application was not started')
        raise ConnectionError