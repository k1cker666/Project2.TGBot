import redis
from redis import exceptions
import logging

def create_connectrion(db_host='redis', db_port=6379, decode_responses=True):
    logger = logging.getLogger(__name__)
    connection = redis.Redis(
        host = db_host,
        port = db_port,
        decode_responses = decode_responses
    )
    try:
        connection.ping()
        logger.info('Connection to Redis DB successful')
    except exceptions.ConnectionError as e:
        logger.info(f'{e}')