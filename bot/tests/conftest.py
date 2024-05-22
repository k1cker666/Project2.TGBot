import pytest
import redis
from src.components.envconfig import load_config
from src.db.psql import create_connection_pool


@pytest.fixture(scope="session")
def config_init():
    config = load_config()
    config.redis.ttl = 1
    return config


@pytest.fixture(scope="session")
def redis_connect(config_init):
    config = config_init.redis
    conn = redis.Redis(
        host=config.host,
        port=config.port,
        decode_responses=True,
        encoding="utf-8",
    )
    return conn


@pytest.fixture(scope="session")
def psql_connect(config_init):
    config = config_init.psql
    pool = create_connection_pool(config)
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                truncate words_in_progress cascade;
                truncate users cascade;
                truncate words cascade;
                """
            )
            conn.commit()
    yield pool
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                truncate words_in_progress restart identity cascade;
                truncate users restart identity cascade;
                truncate words restart identity cascade;
                """
            )
            conn.commit()
    pool.close()


@pytest.fixture(scope="session")
def setup_users_table(psql_connect):
    with psql_connect.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            insert into users (user_id, tg_login, login, password, words_in_lesson, native_language, language_to_learn, word_level)
            values (1, '@test', 'test', 'test', 4, 'ru', 'en', 'A1')
            on conflict do nothing;
            """
            )
        conn.commit()


@pytest.fixture(scope="session")
def setup_words_table(psql_connect):
    with psql_connect.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            insert into words (word_id, language, level, word) VALUES (1, 'ru', 'A1', 'тест1')
            on conflict do nothing;
            insert into words (word_id, language, level, word) VALUES (1, 'en', 'A1', 'test1')
            on conflict do nothing;
            insert into words (word_id, language, level, word) values (2, 'ru', 'A1', 'тест2')
            on conflict do nothing;
            insert into words (word_id, language, level, word) values (2, 'en', 'A1', 'test2')
            on conflict do nothing;
            insert into words (word_id, language, level, word) values (3, 'ru', 'A1', 'тест3')
            on conflict do nothing;
            insert into words (word_id, language, level, word) values (3, 'en', 'A1', 'test3')
            on conflict do nothing;
            insert into words (word_id, language, level, word) values (4, 'ru', 'A1', 'тест4')
            on conflict do nothing;
            insert into words (word_id, language, level, word) values (4, 'en', 'A1', 'test4')
            on conflict do nothing;
            insert into words_in_progress (user_id, word_id, language, number_of_repetitions) values (1, 1, 'en', 3)
            on conflict do nothing;
            """
            )
        conn.commit()
