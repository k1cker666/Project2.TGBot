from src.db import psql, redis

class Dependencies:

    def __init__(self, psql_connect, redis_connect):
        self.psql_connect = psql_connect
        self.redis_connect = redis_connect
    
class DependenciesBuilder:
    
    def build():
        psql_connect = psql.create_connection()
        redis_connect = redis.create_connectrion()
        return Dependencies(psql_connect=psql_connect, redis_connect=redis_connect)