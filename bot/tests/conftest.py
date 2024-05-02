import pytest
import redis
from src.db.psql import create_connection_pool
from src.components.config import load_config

@pytest.fixture(scope="session")
def config_init():
    config = load_config()
    config.redis.ttl = 1
    return config

@pytest.fixture(scope="session")
def redis_connect(config_init):
    config = config_init.redis
    conn = redis.Redis(
        host = config.host,
        port = config.port,
        decode_responses = True,
        encoding = "utf-8")
    return conn
    
@pytest.fixture(scope="session")
def psql_connect(config_init):
    config = config_init.psql
    pool = create_connection_pool(config)
    return pool

@pytest.fixture(scope="session")
def setup_users_table(psql_connect):
    with psql_connect.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            do $$
            begin
                if not exists (
                    select 1 from users
                    where tg_login = '@k1cker666') then
                    insert into users (tg_login, login, password, words_in_lesson, native_language, language_to_learn, word_level)
                    VALUES ('@k1cker666', 'admin', 'admin', 15, 'ru', 'en', 'A1');
                end if;
            end
            $$;""")
        
@pytest.fixture(scope="session")
def setup_words_table(psql_connect):
    with psql_connect.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
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
                if not exists (
                    select 1 from words
                    where word = 'делать') then
                    insert into words (word_id, language, level, word) values (2, 'ru', 'A1', 'делать');
                end if;
                if not exists (
                    select 1 from words
                    where word = 'do') then
                    insert into words (word_id, language, level, word) values (2, 'en', 'A1', 'do');
                end if;
                if not exists (
                    select 1 from words
                    where word = 'думать') then
                    insert into words (word_id, language, level, word) values (3, 'ru', 'A1', 'думать');
                end if;
                if not exists (
                    select 1 from words
                    where word = 'think') then
                    insert into words (word_id, language, level, word) values (3, 'en', 'A1', 'think');
                end if;
                if not exists (
                    select 1 from words
                    where word = 'идти') then
                    insert into words (word_id, language, level, word) values (4, 'ru', 'A1', 'идти');
                end if;
                if not exists (
                    select 1 from words
                    where word = 'go') then
                    insert into words (word_id, language, level, word) values (4, 'en', 'A1', 'go');
                end if;
                if not exists (
                    select 1 from words_in_progress
                    where word_id = 1 and user_id = 1 and language = 'en') then
                    insert into words_in_progress (user_id, word_id, language, number_of_repetitions) values (1, 1, 'en', 3);
                end if;
            end
            $$;""")