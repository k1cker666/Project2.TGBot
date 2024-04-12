from datetime import timedelta
from enum import Enum, auto
import redis
from src.components.config import RedisDB

class UserStateProcessor:
    
    class State(Enum):
        lesson_active = auto()
        lesson_inactive = auto()
    
    conn: redis.Redis
    config: RedisDB
    
    def __init__(self, connection: redis.Redis, config: RedisDB):
        self.conn = connection
        self.config = config
    
    def set_state(self, user_id: str, state: State):
        self.conn.hset(f'{user_id}', 'state', state.name)
        ttl = timedelta(minutes=self.config.ttl)
        self.conn.expire(name=f'{user_id}', time=ttl)
    
    def get_state(self, user_id: str) -> State:
        return self.conn.hget(user_id, 'state')
    
    def set_data(self, user_id: str, data: str):
        self.conn.hset(f'{user_id}', 'data', data)
        ttl = timedelta(minutes=self.config.ttl)
        self.conn.expire(name=f'{user_id}', time=ttl)
    
    def get_data(self, user_id: str) -> dict:
        return self.conn.hgetall(user_id)