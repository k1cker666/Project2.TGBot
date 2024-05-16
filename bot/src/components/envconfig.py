from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class PostgresDB(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="psql_", env_file_encoding="utf-8"
    )
    dbname: str
    user: str
    password: str
    host: str
    port: str
    pool_max_size: int


class RedisDB(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="redis_", env_file_encoding="utf-8"
    )
    host: str
    port: int
    ttl: int


class EnvConfig(BaseSettings):
    bot_token: str
    common_word_count: int
    psql: PostgresDB = PostgresDB()
    redis: RedisDB = RedisDB()


def load_config() -> EnvConfig:
    return EnvConfig()
