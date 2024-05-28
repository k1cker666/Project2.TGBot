from sqlalchemy import Engine, create_engine, insert, select, update
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
            query = select(users).filter_by(login=login)
            result = conn.execute(query)
            result = result.one_or_none()
        return not bool(result)

    def add_user_in_database(
        self,
        tg_login: str,
        login: str,
        password: str,
        words_in_lesson,
        word_level,
    ):
        with self.engine.connect() as conn:
            query = insert(users).values(
                tg_login=tg_login,
                login=login,
                password=password,
                words_in_lesson=words_in_lesson,
                native_language="ru",
                language_to_learn="en",
                word_level=word_level,
            )
            conn.execute(query)
            conn.commit()

    def fetch_user_by_login(self, login: str) -> dict | None:
        with self.engine.connect() as conn:
            query = select(users).filter_by(login=login)
            row = conn.execute(query)
            res = row.one_or_none()
        return None if res is None else res._asdict()

    def update_user_tg_login(self, tg_login: str, login: str):
        with self.engine.connect() as conn:
            query = (
                update(users).values(tg_login=tg_login).filter_by(login=login)
            )
            conn.execute(query)
            conn.commit()

    def clear_tg_login(self, tg_login: str):
        with self.engine.connect() as conn:
            query = (
                update(users)
                .values(tg_login=None)
                .filter_by(tg_login=tg_login)
            )
            conn.execute(query)
            conn.commit()
