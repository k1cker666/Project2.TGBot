from src.components.envconfig import EnvConfig, load_config
from src.components.psql import PostgreSQL
from src.components.redis import Redis


class Dependencies:
    config: EnvConfig
    postgres: PostgreSQL
    redis: Redis

    def __init__(self, config: EnvConfig, postgres: PostgreSQL, redis: Redis):
        self.config = config
        self.postgres = postgres
        self.redis = redis


class DependenciesBuilder:

    def build() -> Dependencies:

        config = load_config()

        postgres = PostgreSQL(config=config.psql)

        redis = Redis(config=config.redis)

        return Dependencies(config=config, postgres=postgres, redis=redis)
