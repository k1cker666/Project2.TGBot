from src.components.envconfig import EnvConfig, load_config
from src.components.psql_core import PostgreSQL
from src.components.redis import Redis


class Dependencies:

    config: EnvConfig
    redis: Redis
    postgres: PostgreSQL

    def __init__(self, config: EnvConfig, redis: Redis, postgres: PostgreSQL):
        self.config = config
        self.redis = redis
        self.postgres = postgres


class DependenciesBuilder:

    def build() -> Dependencies:

        config = load_config()

        redis = Redis(config=config.redis)

        postgres = PostgreSQL(config=config.psql)

        return Dependencies(config=config, redis=redis, postgres=postgres)
