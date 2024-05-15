import os

from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()


class PostgresDB(BaseModel):
    dbname: str = os.getenv("PSQL_DBNAME")
    user: str = os.getenv("PSQL_USER")
    password: str = os.getenv("PSQL_PASSWORD")
    host: str = os.getenv("PSQL_HOST")
    port: str = os.getenv("PSQL_PORT")
    pool_max_size: int = int(os.getenv("PSQL_POOL_MAX_COUNT"))


class RedisDB(BaseModel):
    host: str = os.getenv("REDIS_HOST")
    port: int = int(os.getenv("REDIS_PORT"))
    ttl: int = int(os.getenv("REDIS_TTL"))


class EnvConfig(BaseModel):
    bot_token: str = os.getenv("BOT_TOKEN")
    common_word_count: int = int(os.getenv("COMMON_WORD_COUNT"))
    psql: PostgresDB = PostgresDB()
    redis: RedisDB = RedisDB()


def load_config() -> EnvConfig:
    return EnvConfig()
