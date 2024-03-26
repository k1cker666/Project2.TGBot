import redis
from redis.exceptions import ConnectionError
import logging

def create_connectrion(db_host='localhost', db_port=6379, decode_responses=True): # db_host='localhost'/'redis'
    logger = logging.getLogger(__name__)
    connection = redis.Redis(
        host = db_host,
        port = db_port,
        decode_responses = decode_responses
    )
    try:
        connection.ping()
        logger.info('Connection to Redis DB successful')
    except ConnectionError as e:
        logger.error(f'{e}')
        logger.info('Application was not started')
        raise ConnectionError