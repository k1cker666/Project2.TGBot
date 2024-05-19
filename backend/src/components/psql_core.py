from sqlalchemy import Engine, create_engine, select
from sqlalchemy.exc import OperationalError
from src.components.envconfig import PostgreSQLConfig
from src.models import metadata, users


class PostgreSQL:

    engine: Engine

    def __init__(self, config: PostgreSQLConfig) -> None:
        self.engine = create_engine(
            url=config.get_conninfo(),
            echo=False,
            pool_size=config.pool_max_size,
            max_overflow=5,
        )

    def create_tables(self):
        metadata.create_all(self.engine)

    def check_connect(self):
        try:
            conn = self.engine.connect()
        except OperationalError:
            return False
        else:
            conn.close()
            return True

    def is_login_available(self, login: str) -> bool:
        with self.engine.connect() as conn:
            stmt = select(users).filter_by(login=login)
            result = conn.execute(stmt)
            result = result.one_or_none()
        return not bool(result)
