from random import randint
from typing import List
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
                    "select * from words where word_id = %s and language = %s;",
                    (id, language)
                )
                result = cur.fetchone()
                return result
    
    def fetch_words_for_lesson(
        self,
        user_id: int,
        word_language: str,
        word_level: str,
        words_in_lesson: int
    ) -> List[Word] | None:
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
                    order by random()
                    limit %s;
                    """, (user_id, word_language, word_level, words_in_lesson))
                result = cur.fetchmany(size = words_in_lesson)
                return result if len(result) != 0 else None
            
    def fetch_words_for_answer(
        self,
        word: str,
        language: str
    ) -> List[str]:
        with self.connection_pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    select word, word_similarity(word, %s) as sml
                    from words
                    where language = %s and word != %s
                    order by sml desc
                    limit 3;
                    """, (word, language, word))
                result = cur.fetchmany(size=3)
        answers = [answer[0].capitalize() for answer in result]
        answers.insert(randint(0,3), word.capitalize())
        return answers
    
    def fetch_words_for_repetition(
        self,
        user_id: int,
        word_language: str,
        words_in_lesson: int
    ) -> List[Word] | None:
        with self.connection_pool.connection() as conn:
            with conn.cursor(row_factory=class_row(Word)) as cur:
                cur.execute("""
                    select words.word_id, words.language, level, word from words_in_progress
                    inner join words
                    on words_in_progress.word_id = words.word_id
                    and words_in_progress.language = words.language
                    and user_id = %s
                    where words_in_progress.language = %s
                    and words_in_progress.number_of_repetitions != 0
                    order by random()
                    limit %s;
                    """, (user_id, word_language, words_in_lesson))
                result = cur.fetchmany(size=words_in_lesson)
                return result if len(result) != 0 else None
            
    def fetch_count_learned_words(
        self,
        user_id: int,
        language_to_learn: str
    ) -> int:
        with self.connection_pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    select count(*) from words_in_progress
                    where user_id = %s
                    and language = %s
                    and number_of_repetitions = 0;
                    """, (user_id, language_to_learn))
                result = cur.fetchone()
                return result[0]
            
    def fetch_count_passed_words(
        self,
        user_id: int,
        language_to_learn: str
    ) -> int:
        with self.connection_pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    select count(*) from words_in_progress
                    where user_id = %s
                    and language = %s
                    and number_of_repetitions != 0;
                    """, (user_id, language_to_learn))
                result = cur.fetchone()
                return result[0]
            
    def add_word_in_word_in_progress(
        self,
        user_id: int,
        word_id: int,
        language: str
    ):
        with self.connection_pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    insert into word_in_progress (user_id, word_id, language, number_of_repetitions)
                    values (%s, %s, %s, 3);
                    """, (user_id, word_id, language))
                conn.commit()
                
    def decrease_numder_of_repetitions(
        self,
        user_id: int,
        word_id: int,
        language: str
    ):
        with self.connection_pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    update word_in_progress set number_of_repetitions = number_of_repetitions-1
                    where user_id = %s
                    and word_id = %s
                    and language = %s
                    """, (user_id, word_id, language))
                conn.commit()
                
    def is_current_level_empty(
        self,
        user_id: int,
        language: str
    ) -> bool:
        with self.connection_pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    select count(*) from words
                    left join words_in_progress wip
                    on words.word_id = wip.word_id
                    and words.language = wip.language
                    and wip.user_id = %s
                    where wip is null
                    and words.language = %s
                    """, (user_id, language))
                result = cur.fetchone()
                return result[0]==0