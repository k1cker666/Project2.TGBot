import psycopg
from src.models.word import Word

class WordRepository:
    
    connection: psycopg.Connection
    
    def __init__(self, connection):
        self.connection = connection
        
    def fetch(self, id):
        with self.connection.cursor() as cur:
            cur.execute(
                "select * from tgbot.words where word_id = %s",
                (id,)
            )
            result = cur.fetchone()
            if result != None:
                return Word(
                    word_id = result[0],
                    language = result[1],
                    level = result[2],
                    word = result[3]
                )
            else:
                return result