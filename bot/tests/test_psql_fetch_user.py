import pytest
from src.repository.user_repository import UserRepository

@pytest.mark.parametrize(
    "id, res",
    [
        (1, '@k1cker666'),
        (1.0, '@k1cker666')
    ]
)
def test_fetch_user(create_psql_connect, setup_users_table, id, res):
    conn = create_psql_connect
    setup_users_table
    user_repo = UserRepository(conn)
    assert user_repo.fetch(id).tg_login == res

@pytest.mark.parametrize(
    "id, res",
    [
        (0, None),
        (-10, None)
    ]
)
def test_fetch_nonetype(create_psql_connect, id, res):
    conn = create_psql_connect
    user_repo = UserRepository(conn)
    assert user_repo.fetch(id) == res