from sqlalchemy import Engine, create_engine, insert, select
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

    def add_user_in_database(
        self, tg_login: str, login: str, password: str, words_in_lesson
    ):
        with self.engine.connect() as conn:
            stmt = insert(users).values(
                tg_login=tg_login,
                login=login,
                password=password,
                words_in_lesson=words_in_lesson,
                native_language="ru",
                language_to_learn="en",
                word_level="A1",
            )
            conn.execute(stmt)
            conn.commit()

    def fetch_user_by_login(self, login: str) -> dict | None:
        with self.engine.connect() as conn:
            stmt = select(users).filter_by(login=login)
            row = conn.execute(stmt)
            res = row.one_or_none()
        return None if res is None else res._asdict()
