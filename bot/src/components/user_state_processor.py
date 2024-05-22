import json
from datetime import timedelta
from enum import Enum, auto

import redis
from src.components.envconfig import RedisDB


class State(Enum):
    lesson_active = auto()
    lesson_inactive = auto()


class UserStateProcessor:

    conn: redis.Redis
    config: RedisDB

    def __init__(self, connection: redis.Redis, config: RedisDB):
        self.conn = connection
        self.config = config

    def set_state(self, user_id: str, state: State):
        self.conn.hset(f"{user_id}", "state", state.name)
        ttl = timedelta(minutes=self.config.ttl)
        self.conn.expire(name=f"{user_id}", time=ttl)

    def get_state(self, user_id: str) -> State:
        return self.conn.hget(user_id, "state")

    def set_data(self, user_id: str, data: dict):
        self.conn.hset(f"{user_id}", "data", json.dumps(data))
        ttl = timedelta(minutes=self.config.ttl)
        self.conn.expire(name=f"{user_id}", time=ttl)

    def get_data(self, user_id: str) -> dict:
        data = self.conn.hget(user_id, "data")
        return json.loads(data) if data else None

    def is_user_online(self, user_id: str) -> bool:
        online = self.conn.exists(user_id)
        return True if online else False
