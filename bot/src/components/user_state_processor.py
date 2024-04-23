from datetime import timedelta
from enum import Enum, auto
import redis
from src.components.config import RedisDB
import json

class State(Enum):
    lesson_active = auto()
    lesson_inactive = auto()

class UserStateProcessor:
    
    conn: redis.Redis
    config: RedisDB
    
    def __init__(self, connection: redis.Redis, config: RedisDB):
        self.conn = connection
        self.config = config
    
    def set_state(self, user_id: str, state: State, ttl: int = None):
        self.conn.hset(f'{user_id}', 'state', state.name)
        _ttl = timedelta(minutes=self.config.ttl) if not ttl else timedelta(minutes=ttl)
        self.conn.expire(name=f'{user_id}', time=_ttl)
    
    def get_state(self, user_id: str) -> State:
        return self.conn.hget(user_id, 'state')
    
    def set_data(self, user_id: str, data: dict, ttl: int = None):
        self.conn.hset(f'{user_id}', 'data', json.dumps(data))
        _ttl = timedelta(minutes=self.config.ttl) if not ttl else timedelta(minutes=ttl)
        self.conn.expire(name=f'{user_id}', time=_ttl)
    
    def get_data(self, user_id: str) -> dict:
        data = self.conn.hget(user_id, 'data')
        return json.loads(data) if data else None