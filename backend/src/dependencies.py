from src.components.envconfig import EnvConfig, load_config
from src.components.psql import PostgreSQL


class Dependencies:
    config: EnvConfig
    postgres: PostgreSQL

    def __init__(self, config: EnvConfig, postgres: PostgreSQL):
        self.config = config
        self.postgres = postgres


class DependenciesBuilder:

    def build() -> Dependencies:

        config = load_config()

        postgres = PostgreSQL(config=config.psql)

        return Dependencies(config=config, postgres=postgres)
