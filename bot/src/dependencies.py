from src.db import psql, redis
from src.components.start_handler import StartHandler
from redis import Redis
from psycopg import Connection
from src.repository.word_repository import WordRepository


class Dependencies:

    psql_connect: Connection
    redis_connec: Redis
    start_handler: StartHandler
    word_repository: WordRepository
    
    def __init__(
        self,
        psql_connect,
        redis_connect,
        start_handler,
        word_repository
    ):
        self.psql_connect = psql_connect
        self.redis_connect = redis_connect
        self.start_handler = start_handler
        self.word_repository=word_repository
    
class DependenciesBuilder:
    
    def build():
        psql_connect = psql.create_connection()
        redis_connect = redis.create_connectrion()
        start_handler = StartHandler()
        word_repository = WordRepository(connection=psql_connect)
        return Dependencies(
            psql_connect=psql_connect,
            redis_connect=redis_connect,
            start_handler=start_handler,
            word_repository=word_repository
        )