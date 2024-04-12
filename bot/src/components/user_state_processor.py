from datetime import timedelta
from enum import Enum, auto
import redis

class State(Enum):
    lesson_active = auto()
    lesson_inactive = auto()

class UserStateProcessor:
    
    conn: redis.Redis
    
    def __init__(self, connecton: redis.Redis):
        self.conn = connecton
    
    def set_state(self, user_id: str, state: State):
        self.conn.hset(f'{user_id}', 'state', state.name)
        ttl = timedelta(minutes=10)
        self.conn.expire(name=f'{user_id}', time=ttl)
    
    def get_state(self, user_id: str) -> State:
        return self.conn.hget(user_id, 'state')
    
    def set_data(self, user_id: str, data: str):
        self.conn.hset(f'{user_id}', 'data', data)
        ttl = timedelta(minutes=10)
        self.conn.expire(name=f'{user_id}', time=ttl)
    
    def get_data(self, user_id: str) -> dict:
        return self.conn.hgetall(user_id)