import psycopg_pool
from src.models.user import User
from psycopg.rows import class_row

class UserRepository:
    
    connection_pool: psycopg_pool.ConnectionPool
    
    def __init__(
        self,
        connection_pool: psycopg_pool.ConnectionPool
        ):
        self.connection_pool = connection_pool
        
    def fetch(self, id: int) -> User:
        with self.connection_pool.connection() as conn:
            with conn.cursor(row_factory=class_row(User)) as cur:
                cur.execute(
                    "select * from users where user_id = %s",
                    (id,)
                )
                result = cur.fetchone()
                return result
            
    def fetch_tg_login(self, tg_login: str) -> User:
        with self.connection_pool.connection() as conn:
            with conn.cursor(row_factory=class_row(User)) as cur:
                cur.execute(
                    "select * from users where tg_login = %s",
                    (tg_login,)
                )
                result = cur.fetchone()
                return result