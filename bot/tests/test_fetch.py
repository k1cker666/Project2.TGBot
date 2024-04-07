import pytest
from src.repository.word_repository import WordRepository
import psycopg

@pytest.mark.parametrize(
    "id, language, res",
    [
        (1, 'en', 'hello'),
        (1, 'ru', 'привет'),
        ("1", 'ru', 'привет')
    ]
)
def test_fetch_word(id, language, res):
    with psycopg.connect(
        dbname = 'tgbot',
        user = 'postgres',
        password = 'roma1234',
        host = 'localhost',
        port = '5432',
        autocommit = True) as conn:
        with conn.cursor() as curs:
            curs.execute("""
            do $$
            begin
                if not exists (
                    select 1 from words
                    where word = 'привет') then
                    insert into words (word_id, language, level, word) VALUES (1, 'ru', 'A1', 'привет');
                end if;
                if not exists (
                    select 1 from words
                    where word = 'hello') then
                    insert into words (word_id, language, level, word) VALUES (1, 'en', 'A1', 'hello');
                end if;
            end
            $$;""")
        word_repo = WordRepository(conn)
        assert word_repo.fetch(id, language).word == res

@pytest.mark.parametrize(
    "id, language, res",
    [
        (0, 'en', None),
        (100, 'ru', None),
        ("10", 'ru', None)
    ]
)
def test_fetch_nonetype(id, language, res):
    with psycopg.connect(
        dbname = 'tgbot',
        user = 'postgres',
        password = 'roma1234',
        host = 'localhost',
        port = '5432',
        autocommit = True) as conn:
        word_repo = WordRepository(conn)
        assert word_repo.fetch(id, language) == res