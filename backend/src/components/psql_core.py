from sqlalchemy import Engine, create_engine
from src.components.envconfig import PostgreSQLConfig
from src.models import metadata


class PostgreSQL:

    engine: Engine

    def __init__(self, config: PostgreSQLConfig) -> None:
        self.engine = create_engine(
            url=config.get_conninfo(),
            echo=True,
            pool_size=config.pool_max_size,
            max_overflow=5,
        )

    def create_tables(self):
        metadata.create_all(self.engine)
