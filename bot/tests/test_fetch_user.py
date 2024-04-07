import pytest
from src.repository.user_repository import UserRepository
import psycopg

@pytest.mark.parametrize(
    "id, res",
    [
        (1, '@k1cker666'),
        (1.0, '@k1cker666')
    ]
)
def test_fetch_user(id, res):
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
                    select 1 from users
                    where tg_login = '@k1cker666') then
                    insert into users (tg_login, login, password, words_in_lesson, native_language, language_to_learn)
                    VALUES ('@k1cker666', 'admin', 'admin', 15, 'ru', 'en');
                end if;
            end
            $$;""")
        user_repo = UserRepository(conn)
        assert user_repo.fetch(id).tg_login == res

@pytest.mark.parametrize(
    "id, res",
    [
        (0, None),
        (-10, None)
    ]
)
def test_fetch_nonetype(id, res):
    with psycopg.connect(
        dbname = 'tgbot',
        user = 'postgres',
        password = 'roma1234',
        host = 'localhost',
        port = '5432',
        autocommit = True) as conn:
        user_repo = UserRepository(conn)
        assert user_repo.fetch(id) == res