from src.db import psql, redis
from src.components.start_handler import StartHedler

class Dependencies:

    def __init__(
        self,
        psql_connect,
        redis_connect,
        start_hendler
    ):
        self.psql_connect = psql_connect
        self.redis_connect = redis_connect
        self.start_hendler = start_hendler
    
class DependenciesBuilder:
    
    def build():
        psql_connect = psql.create_connection()
        redis_connect = redis.create_connectrion()
        start_hendler = StartHedler
        return Dependencies(
            psql_connect=psql_connect,
            redis_connect=redis_connect,
            start_hendler=start_hendler
        )