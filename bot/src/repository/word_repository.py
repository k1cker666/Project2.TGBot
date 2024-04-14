import psycopg
from psycopg.rows import class_row
from src.models.word import Word
from src.models.enums import WordLanguage

class WordRepository:
    
    connection: psycopg.Connection
    
    def __init__(
        self,
        connection: psycopg.Connection
        ):
        self.connection = connection
        
    def fetch(self, id: int, language: WordLanguage) -> Word:
        with self.connection.cursor(row_factory=class_row(Word)) as cur:
            cur.execute(
                "select * from words where word_id = %s and language = %s",
                (id, language)
            )
            result = cur.fetchone()
            return result