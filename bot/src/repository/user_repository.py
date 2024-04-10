import psycopg
from src.models.user import User
from psycopg.rows import class_row

class UserRepository:
    
    connection: psycopg.Connection
    
    def __init__(self, connection):
        self.connection = connection
        
    def fetch(self, id: int) -> User:
        with self.connection.cursor(row_factory=class_row(User)) as cur:
            cur.execute(
                "select * from users where user_id = %s",
                (id,)
            )
            result = cur.fetchone()
            return result