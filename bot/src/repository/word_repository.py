from typing import List
from psycopg.rows import class_row
import psycopg_pool
from src.components.lesson_dto import LessonDTO
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
            
    def fetch_words_for_lesson(self,
                               user_id: int,
                               word_language: str,
                               word_level: str,
                               limit: int) -> List[Word]:
        with self.connection_pool.connection() as conn:
            with conn.cursor(row_factory=class_row(Word)) as cur:
                cur.execute("""
                    select words.word_id, words.language, level, word from words
                    left join words_in_progress
                    on words.word_id = words_in_progress.word_id
                    and words.language = words_in_progress.language
                    and words_in_progress.user_id = %s
                    where words_in_progress is null
                    and words.language=%s
                    and words.level=%s
                    limit %s;
                    """, (user_id, word_language, word_level, limit))
                result = cur.fetchmany(size = limit)
                return result