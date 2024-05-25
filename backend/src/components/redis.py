from datetime import timedelta

import redis
from loguru import logger
from redis.exceptions import ConnectionError
from src.components.envconfig import RedisConfig


class Redis:

    connection: redis.Redis
    config: RedisConfig

    def __init__(self, config: RedisConfig):
        self.config = config
        self.config.ttl = 30
        self.__create_connection()

    def __create_connection(self):
        self.connection = redis.Redis(
            host=self.config.host,
            port=self.config.port,
            decode_responses=True,
            encoding="utf-8",
        )
        try:
            self.connection.ping()
            logger.info(
                f"{self.config.host}:{self.config.port} - Connection to Redis DB successful"
            )
        except ConnectionError as e:
            logger.error(f"{self.config.host}:{self.config.port} - {e}")
            logger.info("Application was not started")
            raise ConnectionError

    def set_tg_login(self, tg_login: str, uuid_token: str):
        self.connection.set(name=uuid_token, value=tg_login)
        ttl = timedelta(minutes=self.config.ttl)
        self.connection.expire(name=uuid_token, time=ttl)

    def is_valid_token(self, uuid_token: str) -> bool:
        res = self.connection.get(uuid_token)
        return bool(res)

    def get_tg_login(self, uuid_token: str) -> str:
        return self.connection.get(uuid_token)

    def clear_data(self, data: str):
        if self.connection.exists(data):
            self.connection.expire(data, 1)
