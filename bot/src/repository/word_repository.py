from psycopg.rows import class_row
import psycopg_pool
from src.models.word import Word
from src.models.enums import WordLanguage

class WordRepository:
    
    connection_pool: psycopg_pool.ConnectionPool
    
    def __init__(
        self,
        connection_pool: psycopg_pool.ConnectionPool
        ):
        self.connection_pool = connection_pool
        
    def fetch(self, id: int, language: WordLanguage) -> Word:
        with self.connection_pool.connection() as conn:
            with conn.cursor(row_factory=class_row(Word)) as cur:
                cur.execute(
                    "select * from words where word_id = %s and language = %s",
                    (id, language)
                )
                result = cur.fetchone()
                return result