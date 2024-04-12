import psycopg
import pytest
import redis
from src.components.user_state_processor import UserStateProcessor
from src.components.config import load_config

@pytest.fixture(scope="session")
def create_user_state_proc_obj():
    config = load_config().redis
    with redis.Redis(
        host = config.host,
        port = config.port,
        decode_responses = True,
        encoding = "utf-8") as conn:
        user_state = UserStateProcessor(connection=conn, config=config)
        return user_state
    
@pytest.fixture(scope="session")
def create_psql_connect():
    config = load_config().psql
    conn = psycopg.connect(
        dbname = config.dbname,
        user = config.user,
        password = config.password,
        host = config.host,
        port = config.port,
        autocommit = True)
    return conn

@pytest.fixture(scope="session")
def setup_users_table(create_psql_connect):
    with create_psql_connect.cursor() as curs:
        curs.execute("""
        do $$
        begin
            if not exists (
                select 1 from users
                where tg_login = '@k1cker666') then
                insert into users (tg_login, login, password, words_in_lesson, native_language, language_to_learn)
                VALUES ('@k1cker666', 'admin', 'admin', 15, 'ru', 'en');
            end if;
        end
        $$;""")
        
@pytest.fixture(scope="session")
def setup_words_table(create_psql_connect):
    with create_psql_connect.cursor() as curs:
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