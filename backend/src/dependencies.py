from src.components.envconfig import EnvConfig, load_config
from src.components.psql_core import PostgreSQL
from src.components.redis import Redis
from src.components.validator import Validator


class Dependencies:

    config: EnvConfig
    redis: Redis
    postgres: PostgreSQL
    validator: Validator

    def __init__(
        self,
        config: EnvConfig,
        redis: Redis,
        postgres: PostgreSQL,
        validator: Validator,
    ):
        self.config = config
        self.redis = redis
        self.postgres = postgres
        self.validator = validator


class DependenciesBuilder:

    def build() -> Dependencies:

        config = load_config()

        redis = Redis(config=config.redis)

        postgres = PostgreSQL(config=config.psql)

        validator = Validator(postgres=postgres)

        return Dependencies(
            config=config,
            redis=redis,
            postgres=postgres,
            validator=validator,
        )
