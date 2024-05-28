import psycopg_pool
from psycopg.rows import class_row
from src.models.user import User


class UserRepository:

    connection_pool: psycopg_pool.ConnectionPool

    def __init__(self, connection_pool: psycopg_pool.ConnectionPool):
        self.connection_pool = connection_pool

    def fetch_user_by_id(self, id: int) -> User:
        with self.connection_pool.connection() as conn:
            with conn.cursor(row_factory=class_row(User)) as cur:
                cur.execute("select * from users where user_id = %s;", (id,))
                result = cur.fetchone()
                return result

    def fetch_user_by_tg_login(self, tg_login: str) -> User:
        with self.connection_pool.connection() as conn:
            with conn.cursor(row_factory=class_row(User)) as cur:
                cur.execute(
                    "select * from users where tg_login = %s;", (tg_login,)
                )
                result = cur.fetchone()
                return result

    def update_user_word_level(
        self, word_level: str, user_id: int = None, tg_login: str = None
    ):
        if user_id is not None:
            with self.connection_pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        update users set word_level = %s
                        where user_id = %s
                        """,
                        (word_level, user_id),
                    )
                    conn.commit()
        if tg_login is not None:
            with self.connection_pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        update users set word_level = %s
                        where tg_login = %s
                        """,
                        (word_level, tg_login),
                    )
                    conn.commit()

    def is_user_authorized(self, tg_login: str) -> bool:
        authorization = bool(self.fetch_user_by_tg_login(tg_login=tg_login))
        return authorization
