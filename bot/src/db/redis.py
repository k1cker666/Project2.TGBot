import redis
from redis import exceptions

def create_connectrion(db_host='localhost', db_port=6379, decode_responses=True):
    connection = redis.Redis(
        host = db_host,
        port = db_port,
        decode_responses = decode_responses
    )
    try:
        connection.ping()
        print('Connection to Redis DB successful')
    except exceptions.ConnectionError as e:
        print(f'Redis: {e}')