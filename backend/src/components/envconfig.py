from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class PostgreSQLConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="psql_", env_file_encoding="utf-8"
    )
    dbname: str
    user: str
    password: str
    host: str
    port: str
    pool_max_size: int

    def get_conninfo(self):
        conninfo = (
            f"postgresql+psycopg://{self.user}:"
            + f"{self.password}@{self.host}:{self.port}/{self.dbname}"
        )
        return conninfo


class RedisConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="redis_", env_file_encoding="utf-8"
    )
    host: str
    port: int
    ttl: int


class EnvConfig(BaseSettings):
    bot_token: str
    common_word_count: int
    backend_url: str
    psql: PostgreSQLConfig = PostgreSQLConfig()
    redis: RedisConfig = RedisConfig()


def load_config() -> EnvConfig:
    return EnvConfig()
