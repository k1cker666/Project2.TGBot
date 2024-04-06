import psycopg
from psycopg.rows import class_row
from src.models.word import Word
class WordRepository:
    
    connection: psycopg.Connection
    
    def __init__(self, connection):
        self.connection = connection
        
    def fetch(self, id):
        with self.connection.cursor(row_factory=class_row(Word)) as cur:
            cur.execute(
                "select * from words where word_id = %s",
                (id,)
            )
            result = cur.fetchone()
            return result