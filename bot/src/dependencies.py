from src.db import psql, redis
from src.components.start_handler import StartHandler

class Dependencies:

    start_handler: StartHandler
    
    def __init__(
        self,
        psql_connect,
        redis_connect,
        start_handler
    ):
        self.psql_connect = psql_connect
        self.redis_connect = redis_connect
        self.start_handler = start_handler
    
class DependenciesBuilder:
    
    def build():
        psql_connect = psql.create_connection()
        redis_connect = redis.create_connectrion()
        start_handler = StartHandler
        return Dependencies(
            psql_connect=psql_connect,
            redis_connect=redis_connect,
            start_handler=start_handler
        )